import requests
from flask import Blueprint, request, jsonify
from services.db import mongo
from utils.validation import validate_recommended

# Define the Blueprint
recommended_bp = Blueprint("users", __name__)

USER_SERVICE_URL = "http://127.0.0.1:8081"

@recommended_bp.route("/<int:userId>/profiles/<int:profileId>/recommendeds", methods=["GET"])
def get_recommendeds(userId, profileId):
    # Verifica che l'utente e il profilo esistano
    try:
        response = requests.get(f"{USER_SERVICE_URL}/users/{userId}/profiles/{profileId}")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 404

    # Logica per recuperare i film raccomandati
    recommended_films = mongo.db.recommendeds.find({"userId": userId, "profileId": profileId})
    return jsonify([film for film in recommended_films]), 200


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
