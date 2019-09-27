from classes import *
from http.server import HTTPServer, BaseHTTPRequestHandler
from json import JSONEncoder
from db_operations import *
import os

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

    #def drink_decoder(obj):
    #    if "__type__" in obj and obj["__type__"] == "Drink":
    #        return Drink(obj["id"], obj["name"], obj["instructions"])
    #    return obj

    #def person_decoder(obj):
    #    if "__type__" in obj and obj["__type__"] == "Person":
    #        return Person(obj["id"], obj["forename"], obj["surname"])
    #    return obj

class MyHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type","text/json")
        self.end_headers()

    def get_content_length(self):
        return int(self.headers["Content-Length"])


class UniversalHandler(MyHandler):
    def do_GET(self):
        self._set_headers()
        items = {}
        
        if self.path.lower() == "/people":
            print("people")
            items = get_people_from_db() 

        elif self.path.lower() == "/drinks":
            print("drinks")
            items = get_drinks_from_db()

        elif self.path.lower() == "/rounds":
            print("drinnks")
            items = get_rounds_from_db()

        jd = json.dumps(items, cls=MyEncoder)        
        self.wfile.write(jd.encode("utf-8"))


    def do_POST(self):
        content_length = self.get_content_length()
        data = json.loads(self.rfile.read(content_length))


        if self.path.lower() == "/people":
            fav_drink = data["fav_drink"]
            person = Person(
                -1, 
                data["first_name"], 
                data["last_name"], 
                Drink(
                    fav_drink["id"], 
                    fav_drink["name"], 
                    fav_drink["instructions"]
                )
            )
            person.insert_to_db()
            person.insert_drinks_pref_to_db()
        
        elif self.path.lower() == "/drinks":
            drink = Drink(-1, data["name"], data["instructions"])

        elif self.path.lower() == "/rounds":
            new_round = Round(
                -1,
                data["active"],
                data["start_time_UTC"],
                data["initiator"]
            )
            new_round.save_round_state_on_start_and_set_id()

        self.send_response(201)
        self.end_headers()

if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, UniversalHandler)
    print("Starting server")
    
    httpd.serve_forever()
