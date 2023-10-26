#!/usr/bin/python3
"""
Index file containing the routes and their function
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def status():
    """return the status of the base route query"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stat():
    """return a json response of all onject counts"""
    return jsonify(
        {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
        })
