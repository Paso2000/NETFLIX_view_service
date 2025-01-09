import requests
from flask import Blueprint, request, jsonify
from services.db import mongo
from utils.validation import validate_view

# Define the Blueprint
view_bp = Blueprint("users", __name__)

CONTENT_SERVICE_URL = "http://content_service:8080/films"

@view_bp.route("/<int:userId>/profiles/<int:profileId>/views", methods=["GET"])
def get_views(userId, profileId):
    """
    Ottieni tutte le visualizzazioni per un determinato utente e profilo,
    includendo i dettagli completi dei film.
    """
    views = list(mongo.db.views.find({"userId": userId, "profileId": profileId}))
    enriched_views = []

    for view in views:
        film_id = view.get("filmId")
        if not film_id:
            continue

        # Effettua la richiesta al servizio contenuti per ottenere i dettagli del film
        try:
            response = requests.get(f"{CONTENT_SERVICE_URL}/{film_id}")
            if response.status_code == 200:
                film_details = response.json()
                view["filmDetails"] = film_details  # Aggiungi i dettagli del film
            else:
                view["filmDetails"] = {"error": "Film not found in content service"}
        except requests.exceptions.RequestException as e:
            view["filmDetails"] = {"error": str(e)}

        view["_id"] = str(view["_id"])  # Converti ObjectId in stringa
        enriched_views.append(view)

    return jsonify(enriched_views), 200


@view_bp.route("/<int:userId>/profiles/<int:profileId>/views", methods=["POST"])
def add_recommended(userId, profileId):
    data = request.json
    # Check if the input is a list or a single object
    if isinstance(data, list):
        errors = []
        for view in data:
            valid, error = validate_view(view)
            if not valid:
                errors.append({"view": view, "error": error})
                continue
            # Insert each valid view into the database
            mongo.db.views.insert_one(view)

        if errors:
            return jsonify({
                "message": "Some views were not added",
                "errors": errors
            }), 400
        return jsonify({"message": "Views added successfully"}), 201
    # Handle a single object
    valid, error = validate_view(data)
    if not valid:
        return jsonify(error), 400
    # Insert the single view into the database
    mongo.db.views.insert_one(data)
    return jsonify({"message": "View added successfully"}), 201

@view_bp.route("/<int:userId>/profiles/<int:profileId>/views/<int:filmId>", methods=["GET"])
def get_actor_by_id(userId,profileId,filmId):
    """
  Ottieni i dettagli completi di un film specifico per un determinato utente e profilo.
  """
    view = mongo.db.views.find_one({
        "filmId": filmId,
        "userId": userId,
        "profileId": profileId,
    })

    if not view:
        return jsonify({"error": "View not found"}), 404

    # Effettua la richiesta al servizio contenuti per ottenere i dettagli del film
    try:
        response = requests.get(f"{CONTENT_SERVICE_URL}/{filmId}")
        if response.status_code == 200:
            film_details = response.json()
            view["_id"] = str(view["_id"])  # Converti ObjectId in stringa
            view["filmDetails"] = film_details
        else:
            return jsonify({"error": "Film not found in content service"}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(view), 200

@view_bp.route("/<int:userId>/profiles/<int:profileId>/views/<int:filmId>", methods=["PUT"])
def update_actor(userId,profileId,filmId):
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
        return jsonify(str(updated_view)), 200
    return jsonify({"error": "View not found"}), 404

@view_bp.route("/<int:userId>/profiles/<int:profileId>/views/<int:filmId>", methods=["DELETE"])
def delete_view(userId,profileId,filmId):

    result = mongo.db.views.delete_one({
        "filmId" : filmId,
        "profileId": profileId
    })
    if result.deleted_count > 0:
        return "deleted", 204
    return jsonify({"error": "View not found"}), 404