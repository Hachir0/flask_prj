from flask import Flask, jsonify, request
from flask.views import MethodView
from db import Session, Announcement
app = Flask("app")

def hello_world():
    return jsonify({"hello": "world"})

class UserView(MethodView):
    def get(self, id: int):
        with Session() as session:
            ancmnt = session.get(Announcement, id)
            if ancmnt is None:
                http_response = jsonify({"error" : "annonce not found"})
                return http_response
            return jsonify(ancmnt.dict)
    
    def post(self):
        json_data = request.json
        with Session() as session:
            ancmnt = Announcement(title=json_data["name"], discription=json_data["discription"],
                        registretion_time=json_data["registretion_time"], owner=json_data["owner"]
            )
            session.add(ancmnt)
            try:
                session.commit()
            except:
                http_response = jsonify({"error":"owner already exist"})
                http_response.status_code = 409
                return http_response
        return ancmnt.id_dict
    
    def patch(self):
        json_data = request.json
        with Session as session:
            ancmnt = session.get(Announcement, id)
            if ancmnt is None:
                http_response = jsonify({"error" : "annonce not found"})
                return http_response
            
            if "title" is json_data:
                ancmnt.title = json_data["title"]
                
            if "discription" is json_data:
                ancmnt.discription = json_data["discription"]
            if "owner" is json_data:
                ancmnt.owner = json_data["owner"]
                
            session.add(ancmnt)
            try:
                session.commit()
            except:
                http_response = jsonify({"error": "owner already exist"})
                http_response.status_code = 409
                return http_response
            
            return jsonify(ancmnt.id_dict)
    
    def delete(self):
        with Session as session:
            ancmnt = session.get(Announcement, id)
            if ancmnt is None:
                http_response = jsonify({"error" : "annonce not found"})
                http_response.status_code = 404
                return http_response
            session.delete(ancmnt)
            session.commit()
            return jsonify({"status":"user deleted"})
        
app.add_url_rule("/hi", view_func=hello_world, methods=["GET"])

app.run()