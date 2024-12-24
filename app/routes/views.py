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