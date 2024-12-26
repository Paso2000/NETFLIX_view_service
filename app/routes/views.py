from flask import Blueprint, request, jsonify
from services.db import mongo
from utils.validation import validate_view

# Define the Blueprint
view_bp = Blueprint("/users", __name__)

@view_bp.route("/<int:userId>/profiles/<int:profileId>/views", methods=["GET"])
def get_views(userId, profileId):

    views = list(mongo.db.views.find())
    profileViews=[]
    for view in views:
        if view.profileId == profileId:
            profileViews.append(str(view["_filmId"]))
    return jsonify(profileViews), 200

@view_bp.route("/<int:userId>/profiles/<int:profileId>/views", methods=["POST"])
def add_recommended(userId, profileId):
    data = request.json
    valid, error = validate_view(data)
    if not valid:
        return jsonify(error), 400
    mongo.db.views.insert_one(data)
    return jsonify({"message": "Recommended added successfully"}), 201

@view_bp.route("/<int:userId>/profiles/<int:profileId>/views/<int:filmId>", methods=["GET"])
def get_actor_by_id(profileId,filmId):

    view = mongo.db.views.find_one({
        "profileId": profileId,
        "_filmId": filmId
    })

    if view:
        return jsonify(str(view["_filmId"])), 200
    return jsonify({"error": "Actor not found"}), 404

@view_bp.route("/<int:userId>/profiles/<int:profileId>/views/<int:filmId>", methods=["PUT"])
def update_actor(userId,profileId,filmId):
    data = request.json
    updated_view = mongo.db.actors.find_one_and_update(
        {
            "profileId": profileId,
            "_filmId": filmId
        },
        {"$set": data},
        return_document=True
    )
    if updated_view:
        return jsonify(str(updated_view["_filmId"])), 200
    return jsonify({"error": "Actor not found"}), 404

@view_bp.route("/<int:userId>/profiles/<int:profileId>/views/<int:filmId>", methods=["DELETE"])
def delete_actor(userId,profileId,filmId):

    result = mongo.db.actors.delete_one({
        "profileId": profileId,
        "_filmId": filmId
    })
    if result.deleted_count > 0:
        return "", 204
    return jsonify({"error": "Actor not found"}), 404