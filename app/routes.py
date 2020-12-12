from flask import request, jsonify, make_response, abort
from app import app
from db import Db

BASE_URL = '/api/v1'

database = Db.init_db()


@app.route('/')
def index():
    return '<h1>Winter Of Code 2020</h1>'

@app.route(BASE_URL+'/register', methods=['POST'])
def register():
    user = request.json
    if Db.authorise_participants(database, user) != None:
        return jsonify({"message": "User already exists"}), 409
    elif Db.add_participants(database, user):
        return jsonify({"message": "User added to database"}), 201
    else:
        return jsonify({"message": "Internal Server error"}), 500

@app.route(BASE_URL+'/login', methods=['POST'])
def login():
    user = request.json
    user_id = Db.authorise_participants(database, user)
    if ( user_id != None):
        return jsonify({"token": Db.get_token(database, user_id)}), 202
    else:
        return jsonify({"message":"User not registered"}), 401
