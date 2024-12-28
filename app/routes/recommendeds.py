from flask import Blueprint, request, jsonify
from services.db import mongo
from utils.validation import validate_recommended

# Define the Blueprint
recommended_bp = Blueprint("users", __name__)

@recommended_bp.route("/<int:userId>/profiles/<int:profileId>/recommendeds", methods=["GET"])
def get_films(userId, profileId):
    return jsonify("reccommends"), 200


@recommended_bp.route("/<int:userId>/profiles/<int:profileId>/recommendeds", methods=["POST"])
def add_recommended(userId, profileId):
    return jsonify({"message": "Recommended added successfully"}), 201


@recommended_bp.route("/<int:userId>/profiles/<int:profileId>/recommendeds/<int:filmId>", methods=["DELETE"])
def delete_actor(userId, profileId, filmId):
    return jsonify({"error": "film not found"}), 404
