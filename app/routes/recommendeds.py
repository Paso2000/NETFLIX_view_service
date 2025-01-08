import requests
from flask import Blueprint, request, jsonify
from services.db import mongo
from utils.validation import validate_view


# Define the Blueprint
recommended_bp = Blueprint("users", __name__)

CONTENT_SERVICE_URL = "http://content_service:8080/films"

@recommended_bp.route("/<int:userId>/profiles/<int:profileId>/recommendeds", methods=["GET"])
def get_recommendeds(userId, profileId):
    """
    Ottieni i film raccomandati per un determinato utente e profilo,
    includendo i dettagli completi dei film.
    """
    recs = list(mongo.db.recommendeds.find({"userId": userId, "profileId": profileId}))
    enriched_recs = []

    for rec in recs:
        film_id = rec.get("filmId")
        if not film_id:
            continue

        # Effettua la richiesta al servizio contenuti per ottenere i dettagli del film
        try:
            response = requests.get(f"{CONTENT_SERVICE_URL}/{film_id}")
            if response.status_code == 200:
                film_details = response.json()
                rec["filmDetails"] = film_details  # Aggiungi i dettagli del film
            else:
                rec["filmDetails"] = {"error": "Film not found in content service"}
        except requests.exceptions.RequestException as e:
            rec["filmDetails"] = {"error": str(e)}

        rec["_id"] = str(rec["_id"])  # Converti ObjectId in stringa
        enriched_recs.append(rec)

    return jsonify(enriched_recs), 200

@recommended_bp.route("/<int:userId>/profiles/<int:profileId>/recommendeds", methods=["POST"])
def add_recommendeds(userId, profileId):
    """
    Aggiungi un film raccomandato per un determinato utente e profilo.
    """
    data = request.json
    # Verifica che tutti i campi richiesti siano presenti
    required_fields = ["filmId", "userId", "profileId"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Verifica che userId e profileId corrispondano ai parametri della rotta
    if data["userId"] != userId or data["profileId"] != profileId:
        return jsonify({"error": "userId and profileId in body must match the route parameters"}), 400

    # Inserisci il film raccomandato nel database
    mongo.db.recommendeds.insert_one({
        "filmId": data["filmId"],
        "userId": data["userId"],
        "profileId": data["profileId"]
    })

    return jsonify({"message": "Recommended film added successfully"}), 201


@recommended_bp.route("/<int:userId>/profiles/<int:profileId>/recommendeds/<int:filmId>", methods=["DELETE"])
def delete_recommendeds(userId, profileId, filmId):

    # Elimina il film raccomandato
    result = mongo.db.recommendeds.delete_one({"userId": userId, "profileId": profileId, "filmId": filmId})
    if result.deleted_count == 0:
        return jsonify({"error": "Film not found"}), 404

    return jsonify({"message": "Recommended deleted successfully"}), 204
