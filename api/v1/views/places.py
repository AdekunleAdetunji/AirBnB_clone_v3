#!/usr/bin/python3
"""view for place"""

from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import make_response
from flask import request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places(city_id):
    """gets all places in a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return make_response(jsonify(places), 200)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """gets a single place item"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_place(place_id):
    """deletes a place item"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """adds a new place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user_id = request.get_json().get("user_id")
    if not user_id:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json().get("name"):
        return make_response(jsonify({"error": "Missing name"}), 400)
    place = Place(**request.get_json())
    place.city_id = city_id
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """updates a place item"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at", "city_id, user_id"]:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
