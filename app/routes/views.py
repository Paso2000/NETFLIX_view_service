from flask import Blueprint, request, jsonify
from services.db import mongo
from utils.validation import validate_view

# Define the Blueprint
view_bp = Blueprint("users", __name__)

@view_bp.route("/<int:userId>/profiles/<int:profileId>/views", methods=["GET"])
def get_views(userId, profileId):
    views = list(mongo.db.views.find())
    for view in views:
        view["_id"] = str(view["_id"])
    return jsonify(views), 200

@view_bp.route("/<int:userId>/profiles/<int:profileId>/views", methods=["POST"])
def add_recommended(userId, profileId):
    data = request.json
    mongo.db.views.insert_one(data)
    valid, error = validate_view(data)
    if not valid:
        return jsonify(error), 400
    return jsonify({"message": "Recommended added successfully"}), 201

@view_bp.route("/<int:userId>/profiles/<int:profileId>/views/<int:filmId>", methods=["GET"])
def get_actor_by_id(userId,profileId,filmId):

    view = mongo.db.views.find_one({
        "filmId": filmId,
        "userId": userId,
        "profileId": profileId,
    })
    if view:

        return jsonify(str(view["filmId"])), 200
    return jsonify({"error": "View not found"}), 404

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