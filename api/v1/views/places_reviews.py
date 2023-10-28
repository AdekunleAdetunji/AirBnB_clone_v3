#!/usr/bin/python3
"""view for reviews"""

from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import make_response
from flask import request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews(place_id):
    """get reviews for a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """get a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_review(review_id):
    """deletes a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """adds a new review"""
    place = storage(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user_id = request.get_json().get("user_id")
    if not user_id:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json().get("text"):
        return make_response(jsonify({"error": "Missing text"}), 400)
    review = Review(**request.get_json())
    review.place_id = place_id
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """updates a review item"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at", "place_id, user_id"]:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
