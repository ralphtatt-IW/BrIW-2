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
 

class UniversalHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type","text/json")
        self.end_headers()

    def get_content_length(self):
        return int(self.headers["Content-Length"])

    def do_GET(self):
        self._set_headers()
        items = {}
        
        if self.path.lower() == "/people":
            items = get_people_from_db() 

        elif self.path.lower() == "/drinks":
            items = get_drinks_from_db()

        elif self.path.lower() == "/rounds":
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
            new_round.insert_to_db()

        self.send_response(201)
        self.end_headers()


class WebRender():
    def do_GET(self):
        self._set_headers()

        if self.path.lower() == "/people":
            people = get_people_from_db()
            
            table_contents = ""
            for person in people:
                table_contents += "<tr>\n"
                table_contents += f"<td>\n{person.full_name}</td>"
                table_contents += f"<td>\n{person.fav_drink.name}</td>\n"
                table_contents += "</tr>\n"
            
            html = f"""
            <!DOCTYPE html>
            <html>
                <head>
                    <title>People</title>
                    <link rel="stylesheet" href="./main.css" /> 
                </head>
                <body>
                    <h1>People</h1>
                    <table border="1">
                        <tr>
                            <th>Name</th>
                            <th>Preferences</th>
                        </tr>
                            {table_contents}
                    </table>
                </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))

            
if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, UniversalHandler)
    print("Starting server")
    
    httpd.serve_forever()
