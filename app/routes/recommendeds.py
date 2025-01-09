import requests
from flask import Blueprint, request, jsonify
from services.db import mongo

# Define the Blueprint
recommended_bp = Blueprint("users", __name__)

# Base URL for the content service
CONTENT_SERVICE_URL = "http://content_service:8080/films"

@recommended_bp.route("/<int:userId>/profiles/<int:profileId>/recommendeds", methods=["GET"])
def get_recommendeds(userId, profileId):
    """
    Retrieve recommended films for a specific user profile, including detailed film information.

    Parameters
    ----------
    userId : int
        The unique identifier of the user.
    profileId : int
        The unique identifier of the user's profile.

    Returns
    -------
    Response
        JSON response containing a list of recommended films with detailed film information.
    """
    recs = list(mongo.db.recommendeds.find({"userId": userId, "profileId": profileId}))
    enriched_recs = []

    for rec in recs:
        film_id = rec.get("filmId")
        if not film_id:
            continue

        # Request film details from the content service
        try:
            response = requests.get(f"{CONTENT_SERVICE_URL}/{film_id}")
            if response.status_code == 200:
                film_details = response.json()
                rec["filmDetails"] = film_details  # Add film details
            else:
                rec["filmDetails"] = {"error": "Film not found in content service"}
        except requests.exceptions.RequestException as e:
            rec["filmDetails"] = {"error": str(e)}

        rec["_id"] = str(rec["_id"])  # Convert ObjectId to string
        enriched_recs.append(rec)

    return jsonify(enriched_recs), 200


@recommended_bp.route("/<int:userId>/profiles/<int:profileId>/recommendeds", methods=["POST"])
def add_recommendeds(userId, profileId):
    """
    Add one or more recommended films for a specific user profile.

    Parameters
    ----------
    userId : int
        The unique identifier of the user.
    profileId : int
        The unique identifier of the user's profile.

    Request Body
    ------------
    JSON
        A list of recommended films or a single recommended film object.

    Returns
    -------
    Response
        - 201: Recommended films added successfully.
        - 400: Validation error for some or all recommended films.
    """
    data = request.json

    # Handle a list of recommended films
    if isinstance(data, list):
        errors = []
        for item in data:
            required_fields = ["filmId", "userId", "profileId"]
            for field in required_fields:
                if field not in item:
                    errors.append({"item": item, "error": f"Missing required field: {field}"})
                    continue

            if item["userId"] != userId or item["profileId"] != profileId:
                errors.append({"item": item, "error": "userId and profileId in body must match the route parameters"})
                continue

            mongo.db.recommendeds.insert_one({
                "filmId": item["filmId"],
                "userId": item["userId"],
                "profileId": item["profileId"]
            })

        if errors:
            return jsonify({
                "message": "Some recommended films were not added",
                "errors": errors
            }), 400

        return jsonify({"message": "Recommended films added successfully"}), 201

    # Handle a single recommended film
    required_fields = ["filmId", "userId", "profileId"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    if data["userId"] != userId or data["profileId"] != profileId:
        return jsonify({"error": "userId and profileId in body must match the route parameters"}), 400

    mongo.db.recommendeds.insert_one({
        "filmId": data["filmId"],
        "userId": data["userId"],
        "profileId": data["profileId"]
    })

    return jsonify({"message": "Recommended film added successfully"}), 201


@recommended_bp.route("/<int:userId>/profiles/<int:profileId>/recommendeds/<int:filmId>", methods=["DELETE"])
def delete_recommendeds(userId, profileId, filmId):
    """
    Delete a specific recommended film for a user profile.

    Parameters
    ----------
    userId : int
        The unique identifier of the user.
    profileId : int
        The unique identifier of the user's profile.
    filmId : int
        The unique identifier of the recommended film.

    Returns
    -------
    Response
        - 204: Recommended film deleted successfully.
        - 404: Film not found.
    """
    result = mongo.db.recommendeds.delete_one({"userId": userId, "profileId": profileId, "filmId": filmId})
    if result.deleted_count == 0:
        return jsonify({"error": "Film not found"}), 404

    return jsonify({"message": "Recommended deleted successfully"}), 204
