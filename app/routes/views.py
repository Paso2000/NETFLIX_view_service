import requests
from flask import Blueprint, request, jsonify
from services.db import mongo
from utils.validation import validate_view

# Define the Blueprint
view_bp = Blueprint("users", __name__)

# Base URL for the content service
CONTENT_SERVICE_URL = "http://content_service:8080/films"

@view_bp.route("/<int:userId>/profiles/<int:profileId>/views", methods=["GET"])
def get_views(userId, profileId):
    """
    Retrieve all film views for a specific user profile, including detailed film information.

    Parameters
    ----------
    userId : int
        The unique identifier of the user.
    profileId : int
        The unique identifier of the user's profile.

    Returns
    -------
    Response
        JSON response containing a list of views with detailed film information.
    """
    views = list(mongo.db.views.find({"userId": userId, "profileId": profileId}))
    enriched_views = []

    for view in views:
        film_id = view.get("filmId")
        if not film_id:
            continue

        # Request film details from the content service
        try:
            response = requests.get(f"{CONTENT_SERVICE_URL}/{film_id}")
            if response.status_code == 200:
                film_details = response.json()
                view["filmDetails"] = film_details  # Add film details
            else:
                view["filmDetails"] = {"error": "Film not found in content service"}
        except requests.exceptions.RequestException as e:
            view["filmDetails"] = {"error": str(e)}

        view["_id"] = str(view["_id"])  # Convert ObjectId to string
        enriched_views.append(view)

    return jsonify(enriched_views), 200


@view_bp.route("/<int:userId>/profiles/<int:profileId>/views", methods=["POST"])
def add_views(userId, profileId):
    """
    Add one or more film views for a specific user profile.

    Parameters
    ----------
    userId : int
        The unique identifier of the user.
    profileId : int
        The unique identifier of the user's profile.

    Request Body
    ------------
    JSON
        A list of views or a single view object.

    Returns
    -------
    Response
        - 201: Views added successfully.
        - 400: Validation error for some or all views.
    """
    data = request.json

    # Handle a list of views
    if isinstance(data, list):
        errors = []
        for view in data:
            valid, error = validate_view(view)
            if not valid:
                errors.append({"view": view, "error": error})
                continue
            mongo.db.views.insert_one(view)

        if errors:
            return jsonify({
                "message": "Some views were not added",
                "errors": errors
            }), 400

        return jsonify({"message": "Views added successfully"}), 201

    # Handle a single view
    valid, error = validate_view(data)
    if not valid:
        return jsonify(error), 400

    mongo.db.views.insert_one(data)
    return jsonify({"message": "View added successfully"}), 201


@view_bp.route("/<int:userId>/profiles/<int:profileId>/views/<int:filmId>", methods=["GET"])
def get_view_by_id(userId, profileId, filmId):
    """
    Retrieve detailed information about a specific film view for a user profile.

    Parameters
    ----------
    userId : int
        The unique identifier of the user.
    profileId : int
        The unique identifier of the user's profile.
    filmId : int
        The unique identifier of the viewed film.

    Returns
    -------
    Response
        - 200: View details with film information.
        - 404: View or film not found.
    """
    view = mongo.db.views.find_one({
        "filmId": filmId,
        "userId": userId,
        "profileId": profileId,
    })

    if not view:
        return jsonify({"error": "View not found"}), 404

    # Request film details from the content service
    try:
        response = requests.get(f"{CONTENT_SERVICE_URL}/{filmId}")
        if response.status_code == 200:
            film_details = response.json()
            view["_id"] = str(view["_id"])  # Convert ObjectId to string
            view["filmDetails"] = film_details
        else:
            return jsonify({"error": "Film not found in content service"}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(view), 200


@view_bp.route("/<int:userId>/profiles/<int:profileId>/views/<int:filmId>", methods=["PUT"])
def update_view(userId, profileId, filmId):
    """
    Update details of a specific film view for a user profile.

    Parameters
    ----------
    userId : int
        The unique identifier of the user.
    profileId : int
        The unique identifier of the user's profile.
    filmId : int
        The unique identifier of the viewed film.

    Request Body
    ------------
    JSON
        The updated view details.

    Returns
    -------
    Response
        - 200: View updated successfully.
        - 404: View not found.
    """
    data = request.json
    updated_view = mongo.db.views.find_one_and_update(
        {
            "filmId": filmId,
            "userId": userId,
            "profileId": profileId,
        },
        {"$set": data},
        return_document=True
    )
    if updated_view:
        updated_view["_id"] = str(updated_view["_id"])  # Convert ObjectId to string
        return jsonify(updated_view), 200
    return jsonify({"error": "View not found"}), 404


@view_bp.route("/<int:userId>/profiles/<int:profileId>/views/<int:filmId>", methods=["DELETE"])
def delete_view(userId, profileId, filmId):
    """
    Delete a specific film view for a user profile.

    Parameters
    ----------
    userId : int
        The unique identifier of the user.
    profileId : int
        The unique identifier of the user's profile.
    filmId : int
        The unique identifier of the viewed film.

    Returns
    -------
    Response
        - 204: View deleted successfully.
        - 404: View not found.
    """
    result = mongo.db.views.delete_one({
        "filmId": filmId,
        "profileId": profileId
    })
    if result.deleted_count > 0:
        return jsonify({"message": "View deleted successfully"}), 204
    return jsonify({"error": "View not found"}), 404
