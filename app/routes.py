from flask import request, jsonify, make_response, abort
from app import app, Db
from flasgger.utils import swag_from

BASE_URL = '/api/v1'

database = Db.init_db()


@app.route(BASE_URL+'/')
def index():
    return make_response(jsonify({"message": "DSC Frames API"})), 201


@app.route(BASE_URL+'/register', methods=['POST'])
@swag_from('../docs/register.yml')
def register():
    user = request.json
    if not Db.check_valid_details(database, user):
        return make_response(jsonify({"status": "fail", "message": "User details invalid"})), 409
    elif Db.add_participants(database, user):
        return make_response(jsonify({"status": "success", "message": "User added to database"})), 201
    else:
        return make_response(jsonify({"status": "fail", "message": "Internal Server error"})), 500


@app.route(BASE_URL+'/login', methods=['POST'])
@swag_from('../docs/login.yml')
def login():
    user = request.json
    user_id = Db.authorise_participants(database, user)
    user_token = Db.get_token(database, user_id)
    if (user_id != None):
        return make_response(jsonify({"token": user_token})), 202
    else:
        return make_response(jsonify({"message": "Login failed"})), 401


@app.route(BASE_URL+'/frames', methods=['POST', 'GET', 'DELETE'])
@swag_from('../docs/getframes.yml', methods=['GET'])
@swag_from('../docs/postframes.yml', methods=['POST'])
def frames():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            responseObject = {
                'message': 'Bearer token malformed.'
            }
            return make_response(jsonify(responseObject)), 401
    else:
        auth_token = ''
    if auth_token:
        if request.method == 'POST':
            frame = request.json['frame']
            if frame:
                responseObject = Db.save_frame(database, auth_token, frame)
                if responseObject != None:
                    return make_response(jsonify(responseObject)), 201
                else:
                    responseObject = {
                        'message': 'Frame cannot be added'
                    }
                    return make_response(jsonify(responseObject)), 401
            else:
                responseObject = {
                    'message': 'Provide valid frame data'
                }
                return make_response(jsonify(responseObject)), 401
        elif request.method == 'GET':
            frames_arr = Db.get_frames(database, auth_token)
            if frames_arr != None:
                responseObject = {
                    'frames': frames_arr
                }
                return make_response(jsonify(responseObject)), 201
            else:
                responseObject = {
                    'message': 'Something went wrong'
                }
                return make_response(jsonify(responseObject)), 401
        elif request.method == 'DELETE':
            frame_id = request.args.get('id')
            if Db.delete_frames(database, auth_token, frame_id):
                responseObject = {
                    'message': 'Frame was deleted successfully'
                }
                return make_response(jsonify(responseObject)), 201
            else:
                responseObject = {
                    'message': 'Frame was not deleted!'
                }
                return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 401
