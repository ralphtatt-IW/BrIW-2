from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

from json import JSONEncoder
from classes import *
from db_operations import *
from datetime import datetime

import unittest
from unittest.mock import MagicMock
 

class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Person):
            return {
               "id": o.id,
               "first_name": o.first_name,
               "last_name": o.last_name,
               "fav_drink": o.fav_drink.__dict__
            }
        elif isinstance(o, Drink):
            return {
                "id": o.id,
                "name": o.name,
                "instructions": o.instructions
            }
        elif isinstance(o, Round):
            return {
                "id": o.id,
                "active": o.isActive(),
                "start_time_utc": o.start_time_UTC.strftime("%Y-%m-%d %H:%M:%S.%f"),
                "initiator": o.initiator
            }  
        else:
            return o.__dict__


app = Flask(__name__, static_url_path="/static")
app.json_encoder = MyJSONEncoder


@app.route("/people", methods=["GET", "POST"])
def handle_people():
    if request.method == "GET":
        #get_people = MagicMock(return_value=[{"id": 1, "first_name": "Greg", "last_name": "Ford"}])
        return jsonify(get_people())
    elif request.method == "POST":
        posted_json = request.get_json()
        first_name = posted_json["first_name"]
        last_name = posted_json["last_name"]

        person_id = insert_person(first_name, last_name)
        if "fav_drink" in posted_json.keys():
            insert_person_drinks_pref(person_id, posted_json["fav_drink"]["id"])
        return '', 201


@app.route("/drinks", methods=["GET", "POST"])
def handle_drinks():
    if request.method == "GET":
        #get_drinks = MagicMock(return_value=[{"id": 3, "name": "water", "instructions": None}])
        return jsonify(get_drinks())
    elif request.method == "POST":
        posted_json = request.get_json()
        name = posted_json["name"]
        instructions = posted_json["instructions"]

        insert_drink(name, instructions)
        return '', 201

@app.route("/rounds", methods=["GET", "POST"])
def handle_rounds():
    dummy_round = Round(1, False, datetime.now(), 1)
    get_rounds = MagicMock(return_value=[dummy_round])

    return jsonify(get_rounds())
    pass


@app.route("/rounds/<round_id>")
def handle_round(round_id):
    return jsonify(get_round_by_id(round_id))


@app.route("/rounds/orders/<round_id>", methods=["GET", "POST"])
def handle_round_orders(round_id):
    if request.method == "GET":
        return jsonify(get_round_orders(round_id))
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
