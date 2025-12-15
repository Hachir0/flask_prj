from flask import Flask, jsonify, request
from flask.views import MethodView
from db import Session, Announcement
from errors import HttpError
from sqlalchemy.exc import IntegrityError
from scheme import CreateAnnouncement, UpdateAnnouncement, validate
app = Flask("app")

@app.before_request
def before_requsest():
    request.session = Session()
    
@app.after_request
def after_request(response):
    request.session.close()
    return response

def insert_db(ancmnt: Announcement):
    try:
        request.session.add(ancmnt)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "announcement already exist")

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.message})
    response.status_code = error.status_code
    return response

def get_ancmnt_by_id(id):
    ancmnt = request.session.get(Announcement, id)
    if ancmnt is None:
        raise HttpError(404, "announcement not found")
    return ancmnt

class UserView(MethodView):
    def get(self, id: int):
        ancmnt = get_ancmnt_by_id(id)
        return jsonify(ancmnt.dict)
    
    def post(self):
        json_data = validate(request.json, CreateAnnouncement)
        ancmnt = Announcement(title=json_data["title"], discription=json_data["discription"],
                              owner=json_data["owner"]
        )
        insert_db(ancmnt=ancmnt)
        return jsonify(ancmnt.id_dict)
    
    def patch(self, id: int):
        json_data = validate(request.json, UpdateAnnouncement)
        ancmnt = get_ancmnt_by_id(id)
        if "title" in json_data:
            ancmnt.title = json_data["title"]
                
        if "discription" in json_data:
            ancmnt.discription = json_data["discription"]
        if "owner" in json_data:
            ancmnt.owner = json_data["owner"]
                
        insert_db(ancmnt=ancmnt)
        # try:
        #     request.session.commit()
        # except IntegrityError:
        #     raise HttpError(409, "announcement already exist")
        

        return jsonify(ancmnt.id_dict)    
        
    
    def delete(self, id: int):
        ancmnt = get_ancmnt_by_id(id)
        request.session.delete(ancmnt)
        request.session.commit()
        return jsonify({"status":"announcement deleted"})
        
# app.add_url_rule("/hi", view_func=hello_world, methods=["GET"])

user_view = UserView.as_view("user_view")

app.add_url_rule(
    "/announcements",
    view_func=user_view,
    methods=["POST"]
)
app.add_url_rule(
    "/announcements/<int:id>",
    view_func=user_view,
    methods=["GET", "PATCH", "DELETE"]
)

app.run()
