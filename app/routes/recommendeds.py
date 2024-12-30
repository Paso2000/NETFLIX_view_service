import requests
from flask import Blueprint, request, jsonify
from services.db import mongo
from utils.validation import validate_recommended

# Define the Blueprint
recommended_bp = Blueprint("users", __name__)

USER_SERVICE_URL = "http://user_service:8081"
CONTENT_SERVICE_URL = "http://content_service:8080"


# torno i film raccomandati per quel profilo
# controllo se ce ci sono entita recommended per user-profilo ID
# chiedo le inforamzioni di quei fil dall filmId
@recommended_bp.route("/<int:userId>/profiles/<int:profileId>/recommendeds", methods=["GET"])
def get_recommendeds(userId, profileId):
    # Recupera i film raccomandati dal database per userId e profileId
    recommendeds = list(mongo.db.recommendeds.find({"userId": userId, "profileId": profileId}))
    if not recommendeds:
        return jsonify({"error": "No recommended films found for this user and profile"}), 404
    # Estrae tutti i filmId dai risultati
    film_ids = [rec["filmId"] for rec in recommendeds]
    # Ottiene le informazioni sui film dal servizio content_service
    try:
        response = requests.get(
            f"{CONTENT_SERVICE_URL}/films/bulk",
            json={"filmIds": film_ids},
        )
        response.raise_for_status()  # Solleva un'eccezione per errori HTTP
        film_details = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch film details: {str(e)}"}), 500

    # Combina i dettagli dei film con i dati raccomandati
    result = []
    for rec in recommendeds:
        film_detail = next((film for film in film_details if film["filmId"] == rec["filmId"]), None)
        if film_detail:
            result.append({
                "userId": userId,
                "profileId": profileId,
                "filmId": rec["filmId"],
                "recommended_at": rec["recommended_at"],
                "film_details": film_detail,
            })

    return jsonify(result), 200


@recommended_bp.route("/<int:userId>/profiles/<int:profileId>/recommendeds", methods=["POST"])
def add_recommendeds(userId, profileId):
    # Verifica che l'utente e il profilo esistano
    try:
        response = requests.get(f"{USER_SERVICE_URL}/users/{userId}/profiles/{profileId}")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 404

    # Aggiungi il film raccomandato
    data = request.json
    data["userId"] = userId
    data["profileId"] = profileId
    mongo.db.recommendeds.insert_one(data)

    return jsonify({"message": "Recommended added successfully"}), 201


@recommended_bp.route("/<int:userId>/profiles/<int:profileId>/recommendeds/<int:filmId>", methods=["DELETE"])
def delete_recommendeds(userId, profileId, filmId):
    # Verifica che l'utente e il profilo esistano
    try:
        response = requests.get(f"{USER_SERVICE_URL}/users/{userId}/profiles/{profileId}")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 404

    # Elimina il film raccomandato
    result = mongo.db.recommendeds.delete_one({"userId": userId, "profileId": profileId, "filmId": filmId})
    if result.deleted_count == 0:
        return jsonify({"error": "Film not found"}), 404

    return jsonify({"message": "Recommended deleted successfully"}), 204
