
from flask import Blueprint, request, jsonify
from services.db import mongo
from utils.validation import validate_recommended
from .views import view_bp

# Define the Blueprint

@view_bp.route("/<int:userId>/profiles/<int:profileId>/views", methods=["GET"])
def get_films(userId, profileId):

    recommendeds = list(mongo.db.recommendeds.find())
    profileRecommended=[]
    for recommended in recommendeds:
        if recommended.profileId == profileId:
            profileRecommended.append(str(recommended["_filmId"]))
    return jsonify(profileRecommended), 200

@view_bp.route("/<int:userId>/profiles/<int:profileId>/views", methods=["POST"])
def add_recommended(userId, profileId):
    data = request.json
    valid, error = validate_recommended(data)
    if not valid:
        return jsonify(error), 400
    mongo.db.recommendeds.insert_one(data)
    return jsonify({"message": "Recommended added successfully"}), 201


