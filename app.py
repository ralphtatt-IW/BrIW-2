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


app = Flask(__name__, static_folder="/templates")
app.json_encoder = MyJSONEncoder


@app.route("/people", methods=["GET", "POST"])
def handle_people():
    if request.method == "GET":
        #get_people_from_db = MagicMock(return_value=[{"id": 1, "first_name": "Greg", "last_name": "Ford"}])
        return jsonify(get_people_from_db())


@app.route("/drinks", methods=["GET", "POST"])
def handle_drinks():
    if request.method == "GET":
        #get_drinks_from_db = MagicMock(return_value=[{"id": 3, "name": "water", "instructions": None}])
        return jsonify(get_drinks_from_db())


@app.route("/rounds", methods=["GET", "POST"])
def handle_rounds():
    return jsonify(get_rounds_from_db())
    pass

@app.route("/rounds/<round_id>")
def handle_round(round_id):
    return jsonify(get_round_from_db_by_id(round_id))


@app.route("/rounds/orders/<round_id>", methods=["GET", "POST"])
def handle_round_orders(round_id):
    if request.method == "GET":
        return jsonify(get_round_orders_from_db(round_id))
    else:
        posted_json = request.get_json()
        person_id = posted_json["person"]
        drink_id = posted_json["drink"]
        add_order_to_db(round_id, person_id, drink_id)
        return "", 201


@app.route("/form", methods=["GET", "POST"])
def handle_form():
    if request.method == "GET":
        return render_template("form.html", title="Add")
    else:
        person_name = request.form.get("person-name")
        drink_name = request.form.get("drink-name")
        
        return render_template("posted.html", title="Record Posted", person_name=person_name, drink_name=drink_name)

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
