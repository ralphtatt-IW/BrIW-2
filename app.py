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
               "fav_drink": o.fav_drink
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


@app.route("/api/people", methods=["GET", "POST"])
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
            print(fav_drink)
            insert_person_drinks_pref(person_id, posted_json["fav_drink"]["id"])
        return '', 201


@app.route("/api/people/<person_id>", methods=["GET", "PUT", "DELETE"])
def handle_person(person_id):
    if request.method == "GET":
        return jsonify(get_person_by_id(person_id))
    elif request.method == "PUT":
        put_json = request.get_json()
        first_name = put_json["first_name"]
        last_name = put_json["last_name"]
        
        update_person(person_id, first_name, last_name)

        if "fav_drink" in put_json.keys():
            fav_drink_id = put_json["fav_drink"]["id"]
            print("updated pref")
            update_pref(person_id, fav_drink_id)
        return '', 200
    elif request.method == "DELETE":

        return '', 204


@app.route("/api/drinks", methods=["GET", "POST"])
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


@app.route("/api/drinks/<drink_id>", methods=["GET", "PUT", "DELETE"])
def handle_drink(drink_id):
    return jsonify(get_drink_by_id(drink_id))


@app.route("/api/rounds", methods=["GET", "POST"])
def handle_rounds():
    #dummy_round = Round(1, False, datetime.now(), 1)
    #get_rounds = MagicMock(return_value=[dummy_round])
    if request.method == "GET":
        return jsonify(get_rounds())
    elif request.method == "POST":
        posted_json = request.get_json()
        active = posted_json["active"]
        start_time_UTC = datetime.strptime(posted_json["start_time_utc"], "%Y-%m-%d %H:%M:%S.%f")
        initiator = posted_json["initiator"]
        
        insert_round(active, start_time_UTC, initiator)
        return '', 201
    

@app.route("/api/rounds/<round_id>", methods=["GET", "PUT"])
def handle_round(round_id):
    return jsonify(get_round_by_id(round_id))


@app.route("/api/rounds/orders/<round_id>", methods=["GET", "POST"])
def handle_round_orders(round_id):
    if request.method == "GET":
        return jsonify(get_round_orders(round_id))
    else:
        posted_json = request.get_json()
        person_id = posted_json["person_id"]
        drink_id = posted_json["drink_id"]
        insert_round_order(round_id, person_id, drink_id)
        return "", 201


@app.route("/")
def serve_home():
    return render_template("index.html")


@app.route("/people", methods=["GET", "POST"])
def serve_people_page():
    if request.method == "GET":
        get_people = MagicMock(return_value=[Person(1, "Greg", "Ford", Drink(3, "Water", None))])
        get_drinks = MagicMock(return_value=[
            Drink(1, "Drink 1", None),
            Drink(2, "Drink 2", None),
            Drink(3, "Drink 3", None),
            Drink(4, "Drink 4", None),
            Drink(5, "Drink 5", None),
            Drink(6, "Drink 6", None),
            Drink(7, "Drink 7", None),
            Drink(8, "Drink 8", None),
            Drink(9, "Drink 9", None),
            Drink(10, "Drink 10", None),
            Drink(11, "Drink 11", None)
        ])
        return render_template("people.html", title="People", people=get_people(), drinks=get_drinks())
    else:
        person_name = request.form.get("person-name")
        drink_name = request.form.get("drink-name")
        
        return render_template("people.html", title="People", person_name=person_name, drink_name=drink_name)

@app.route("/drinks", methods=["GET", "POST"])
def serve_drinks_page():
    if request.method == "GET":
        get_drinks = MagicMock(return_value=[
            Drink(1, "Drink 1", None),
            Drink(2, "Drink 2", None),
            Drink(3, "Drink 3", None),
            Drink(4, "Drink 4", None),
            Drink(5, "Drink 5", None),
            Drink(6, "Drink 6", None),
            Drink(7, "Drink 7", None),
            Drink(8, "Drink 8", None),
            Drink(9, "Drink 9", None),
            Drink(10, "Drink 10", None),
            Drink(11, "Drink 11", None)
        ])
        return render_template("drinks.html", title="Drinks", drinks=get_drinks())


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
