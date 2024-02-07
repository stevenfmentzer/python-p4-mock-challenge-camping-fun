#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return 'hello'

@app.route('/campers', methods=['GET','POST'])
def campers():
    if request.method == 'GET':
        try:
            campers_dict = [camper.to_dict(rules=('-signups',)) for camper in Camper.query.all()]
            print("WE GOT CAMPERS")
            response = make_response(campers_dict, 200)
        except: 
            response = make_response({"ERROR" : "NO CAMPERS FOUND"},404)

    elif request.method == 'POST':
        if request.headers.get("Content-Type") == 'application/json':
            form_data = request.get_json()
        else:
            form_data = request.form

        try: 
            new_camper = Camper(
                name = form_data['name'],
                age = form_data['age']
            )
            db.session.add(new_camper)
            db.session.commit()

            response = make_response(new_camper.to_dict(rules=('-signups',)),201)
        except: 
            response = make_response({"errors" : ["validation errors"]},400)
    return response

@app.route('/campers/<int:id>', methods=['GET', 'PATCH'])
def camper_by_id(id):
    camper = Camper.query.filter(Camper.id == id).first()
    if camper: 
        if request.method == 'GET':
            response = make_response(camper.to_dict(), 201)

        elif request.method == 'PATCH':
            try:
                if request.headers.get("Content-Type") == 'application/json':
                    form_data = request.get_json()
                else:
                    form_data = request.form
                
                for attr in form_data:
                    setattr(camper, attr, form_data[attr])
                db.session.commit()
                response = make_response(camper.to_dict(), 202)
        
            except: 
                response = make_response({"errors" : ["validation errors"]},400)
    else: 
        response = make_response({"error" : "Camper not found"}, 404)

    return response

@app.route('/activities')
def activities():
    activities_dict = [activity.to_dict(rules=('-signups',)) for activity in Activity.query.all()]
    if activities_dict: 
        response = make_response(activities_dict,201)
    else: 
        response = make_response({"ERROR" : "NO ACTIVITES FOUND"})
    return response

@app.route('/activities/<int:id>', methods=['DELETE'])
def activity_by_id(id):
    try:
        activity = Activity.query.filter(Activity.id == id).first()
        db.session.delete(activity)
        db.session.commit()
        response = make_response({},204)
    except: 
        response = make_response({"error" : "Activity not found"},404)
    return response

@app.route('/signups', methods=['POST'])
def signups():
    if request.headers.get("Content-Type") == 'application/json':
        form_data = request.get_json()
    else:
        form_data = request.form

    try: 
        new_signup = Signup(
            time = form_data['time'],
            camper_id = form_data['camper_id'],
            activity_id = form_data['activity_id']
        )
        db.session.add(new_signup)
        db.session.commit()

        response = make_response(new_signup.to_dict(),201)
    except: 
        response = make_response({"errors" : ["validation errors"]},400)

    return response
if __name__ == '__main__':
    app.run(port=5555, debug=True)
