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
    """
      Effettua una richiesta al servizio user_service per recuperare i dettagli
      dell'utente e i profili associati a userId e profileId.
      """
    try:
        # Effettua una richiesta al servizio user_service
        response = requests.get(f"{USER_SERVICE_URL}/users/{userId}")
        response.raise_for_status()  # Solleva un'eccezione per errori HTTP

        # Ottiene i dati dell'utente dalla risposta
        user_data = response.json()
        profiles = user_data.get("profiles", "")

        # Controlla se il profileId richiesto è associato all'utente
        if str(profileId) not in profiles.split(", "):
            return jsonify({"error": f"Profile ID {profileId} not found for User ID {userId}"}), 404

        return jsonify({
            "userId": userId,
            "profileId": profileId,
            "profiles": profiles.split(", "),
        }), 200

    except requests.exceptions.RequestException as e:
        # Gestione degli errori di connessione o HTTP
        return jsonify({"error": f"Failed to fetch user details: {str(e)}"}), 500

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
