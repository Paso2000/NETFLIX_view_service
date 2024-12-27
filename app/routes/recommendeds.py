
from flask import Blueprint, request, jsonify
from services.db import mongo
from utils.validation import validate_recommended
from .views import view_bp

@view_bp.route("/", methods=["GET"])
def get_films(userId, profileId):

    reccommends = list(mongo.db.recommendeds.find())
    for rec in reccommends:
        rec["_id"] = str(rec["_id"])  # Convert ObjectId to string for serialization
    return jsonify(reccommends), 200

@view_bp.route("/<int:userId>", methods=["POST"])
def add_recommended(userId, profileId):
    data = request.json
    valid, error = validate_recommended(data)
    if not valid:
        return jsonify(error), 400
    mongo.db.recommendeds.insert_one(data)
    return jsonify({"message": "Recommended added successfully"}), 201

@view_bp.route("/<int:userId>/profiles/<int:profileId>/recommendeds/<int:filmId>", methods=["DELETE"])
def delete_actor(userId,profileId,filmId):

    result = mongo.db.recommendeds.delete_one({
        "profileId": profileId,
        "_filmId": filmId
    })
    if result.deleted_count > 0:
        return "", 204
    return jsonify({"error": "Actor not found"}), 404




