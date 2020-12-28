from flask import request, jsonify, make_response
from app import app, Db, mail
from utils import Utils
from flasgger.utils import swag_from

BASE_URL = '/api/v1'

database = Db.init_db()


@app.route(BASE_URL + '/')
def index():
    return make_response(jsonify({"message": "DSC Frames API"})), 201


@app.route(BASE_URL + '/send-reset-mail', methods=['POST'])
@swag_from('../docs/sendresetmail.yml')
def send_reset_mail():
    data = request.json
    if 'email' not in data.keys():
        responseObject = {
            'message': 'email not specified in the body'
        }
        return make_response(jsonify(responseObject)), 400
    else:
        emailAddr = data['email']
        userId = Db.check_email_address(database, emailAddr)
        if userId is not None:
            resetLink = f'https://iwasat.events/reset.html?token={Utils.get_reset_token(userId)}'
            Utils.send_reset_password_mail(mail, resetLink, emailAddr)
            responseObject = {
                'message': 'reset link was sent to the respective email address'
            }
            return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'message': 'email doesnot match'
            }
            return make_response(jsonify(responseObject)), 401


@app.route(BASE_URL + '/update-password', methods=['POST'])
@swag_from('../docs/updatepassword.yml')
def update_password():
    data = request.json
    if 'token' not in data.keys() and 'password' not in data.keys():
        responseObject = {
            'message': 'token or password is absent in the request body'
        }
        return make_response(jsonify(responseObject)), 400
    else:
        token = data['token']
        password = data['password']
        userId = Utils.verify_reset_token(token)
        if userId is None:
            responseObject = {
                'message': 'invalid reset token'
            }
            return make_response(jsonify(responseObject)), 401
        else:
            Db.change_password(database, userId, password)
            responseObject = {
                'message': 'password updated successfully'
            }
            return make_response(jsonify(responseObject)), 200


@app.route(BASE_URL + '/register', methods=['POST'])
@swag_from('../docs/register.yml')
def register():
    user = request.json
    if not Db.check_valid_details(database, user):
        return make_response(jsonify({"message": "User details invalid"})), 409
    elif Db.add_participants(database, user):
        return make_response(jsonify({"message": "User added to database"})), 201
    else:
        return make_response(jsonify({"message": "Internal Server error"})), 500


@app.route(BASE_URL + '/login', methods=['POST'])
@swag_from('../docs/login.yml')
def login():
    user = request.json
    user_data = Db.authorise_participants(database, user)
    if (user_data is not None and user_data[0] is not None):
        user_token = Db.get_token(database, user_data[0])
        return make_response(jsonify({"token": user_token, "data": user_data[1]})), 202
    else:
        return make_response(jsonify({"message": "Login failed"})), 401


@app.route(BASE_URL + '/frames', methods=['POST', 'GET', 'DELETE', 'PUT'])
@swag_from('../docs/getframes.yml', methods=['GET'])
@swag_from('../docs/postframes.yml', methods=['POST'])
@swag_from('../docs/deleteframes.yml', methods=['DELETE'])
@swag_from('../docs/updateframes.yml', methods=['PUT'])
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
                if responseObject is not None:
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
                return make_response(jsonify(responseObject)), 400
        elif request.method == 'GET':
            frames_arr = Db.get_frames(database, auth_token)
            if frames_arr is not None:
                responseObject = {
                    'frames': frames_arr
                }
                return make_response(jsonify(responseObject)), 201
            else:
                responseObject = {
                    'message': 'Frames cannot be fetched'
                }
                return make_response(jsonify(responseObject)), 400
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
                return make_response(jsonify(responseObject)), 400
        elif request.method == 'PUT':
            frame_id = request.json['frame_id']
            frame_data = request.json['frame_data']
            upd_frame = Db.update_frames(database, auth_token, frame_id, frame_data)
            if upd_frame is not None:
                responseObject = {
                    'message': 'Frame was updated successfully',
                    'data': upd_frame
                }
                return make_response(jsonify(responseObject)), 201
            else:
                responseObject = {
                    'message': 'Frame cannot be updated',
                }
                return make_response(jsonify(responseObject)), 400
    else:
        responseObject = {
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 401
