from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

import json
from classes import *
from db_operations import *

class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


app = Flask(__name__)
app.json_encoder = MyJSONEncoder

@app.route("/people", methods=["GET", "POST"])
def handle_people():
    if request.method == "GET":
        return jsonify(get_people_from_db())
    
@app.route("/drinks", methods=["GET", "POST"])
def handle_drinks():
    #get drinks
    pass

@app.route("/routes", methods=["GET", "POST"])
def handle_rounds():
    #get rounds
    pass


if __name__ == "__main__":
    app.run(host="localhost", port=8000)
