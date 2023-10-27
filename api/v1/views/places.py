#!/usr/bin/python3

"""
module that contains the views for url interaction with the places table
"""

from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import make_response
from flask import request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("places/<place_id>", strict_slashes=False, methods=["GET"])
@app_views.route("cities/<city_id>/places", strict_slashes=False,
                 methods=["GET"])
def get_place(city_id=None, place_id=None):
    """
    retrieve the places in a city if city_id else return a place with
    given place_id
    """
    if city_id:
        cities = storage.get(City, city_id)
        if not cities:
            abort(404)
        else:
            places = [place.to_dict() for place in cities.places]
            return make_response(jsonify(places), 200)
    else:
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        else:
            return make_response(jsonify(place.to_dict()), 200)


@app_views.route("places/<place_id>", strict_slashes=False, methods=["DELETE"])
def delete_place(place_id):
    """delete a place with a given place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route("cities/<city_id>/places", strict_slashes=False,
                 methods=["POST"])
def create_place(city_id):
    """create a place linked to a user and a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user = storage.get(User, request.get_json().get("user_id"))
    if not user:
        abort(404)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    place = Place(**request.get_json())
    place.city_id = city_id
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("places/<place_id>", strict_slashes=False, methods=["PUT"])
def update_place(place_id):
    """update a place in the places table"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "city_id", "created_at", "update_at"]:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
