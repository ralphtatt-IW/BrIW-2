from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

from json import JSONEncoder
from classes import *
from db_operations import *

import unittest
from unittest.mock import MagicMock
 

class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


app = Flask(__name__)
app.json_encoder = MyJSONEncoder

@app.route("/people", methods=["GET", "POST"])
def handle_people():
    if request.method == "GET":
        get_people_from_db = MagicMock(return_value=[{"id": 1, "first_name": "Greg", "last_name": "Ford"}])
        return jsonify(get_people_from_db())
    
@app.route("/drinks", methods=["GET", "POST"])
def handle_drinks():
    if request.method == "GET":
        get_drinks_from_db = MagicMock(return_value=[{"id": 3, "name": "water", "instructions": None}])
        return jsonify(get_drinks_from_db())

@app.route("/rounds", methods=["GET", "POST"])
def handle_rounds():
    #get rounds
    pass

@app.route("/rounds/orders", methods=["GET", "POST"])
def handle_round_orders():
    #get round orders
    return jsonify({"test": True})


if __name__ == "__main__":
    app.run(host="localhost", port=8000)
