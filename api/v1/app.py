#!/usr/bin/python3
"""
This module contains the flask app that controls our api
"""

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from flask import make_response
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """close connection to the database"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """return a 404 json response"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
