"""
    routes
    ~~~~~~

    Handles all the API endpoints of the app package.
"""


from flask import request, jsonify, make_response
from app import app, Db, mail
from utils import Utils
from flasgger.utils import swag_from

BASE_URL = '/api/v1'

database = Db()


@app.route(BASE_URL + '/')
def index():
    """Simple check endpoint"""
    return make_response(jsonify({"message": "DSC Frames API", "version": "1.0"})), 201


@app.route(BASE_URL + '/send-reset-mail', methods=['POST'])
@swag_from('../docs/sendresetmail.yml')
def send_reset_mail():
    """
    Sending reset mail
    ~~~~~~~~~~~~~~~~~~

    Endpoint to send a reset mail to the user

    Internally
    ----------

    Reads the email address from the request body
    checks if the email address exists in the database
    if it does then calls the utility function to send_reset_password_mail

    Returns
    -------
    make_response, status_code(int)
        The object with the data or message, and a corresponding HTTP status codes

        To get an idea of what each code signifies
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

    """

    data = request.json
    if 'email' not in data.keys():
        responseObject = {
            'message': 'email not specified in the body'
        }
        return make_response(jsonify(responseObject)), 400
    else:
        emailAddr = data['email']
        userId = database.check_email_address(emailAddr)
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
    """
    Update Password
    ~~~~~~~~~~~~~~~

    Endpoint to update the password of a user

    Internally
    ----------

    Token and new password is read from the request body
    Token is verified using the Utility function verify_reset_token
    If it is valid password gets updated using the Db function change_password

    Returns
    -------
    make_response, status_code(int)
        The object with the data or message, and a corresponding HTTP status codes
    """

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
            database.change_password(userId, password)
            responseObject = {
                'message': 'password updated successfully'
            }
            return make_response(jsonify(responseObject)), 200


@app.route(BASE_URL + '/register', methods=['POST'])
@swag_from('../docs/register.yml')
def register():
    """
    Register
    ~~~~~~~~

    Register a new user

    Internally
    ----------
    Checks if the details provided are valid and unique
    If valid then adds the details to the database using Db function add_participants

    Returns
    -------
    make_response, status_code(int)
        The object with the data or message, and a corresponding HTTP status codes
    """

    user = request.json
    if not database.check_valid_details(user):
        return make_response(jsonify({"message": "User details invalid"})), 409
    elif database.add_participants(user):
        return make_response(jsonify({"message": "User added to database"})), 201
    else:
        return make_response(jsonify({"message": "Internal Server error"})), 500


@app.route(BASE_URL + '/login', methods=['POST'])
@swag_from('../docs/login.yml')
def login():
    """
    Login
    ~~~~~

    Logins the user and generates token

    Internally
    ----------

    Reads the email and password from the request body
    Checks if the combinations match
    If it does it generates a token

    Returns
    -------
    make_response, status_code(int)
        The object with the data or message, and a corresponding HTTP status codes
    """

    user = request.json
    user_data = database.authorise_participants(user)
    if (user_data is not None and user_data[0] is not None):
        user_token = Utils.encode_auth_token(user_data[0])
        responseObject = {"token": user_token,
                          "name": user_data[1]['name'],
                          "email": user_data[1]['email'],
                          "role": user_data[1]['role'],
                          "organisation": user_data[1]['organisation']
                          }
        return make_response(jsonify(responseObject)), 202
    else:
        return make_response(jsonify({"message": "Login failed"})), 401


@app.route(BASE_URL + '/frames', methods=['POST', 'GET', 'DELETE', 'PUT'])
@swag_from('../docs/getframes.yml', methods=['GET'])
@swag_from('../docs/postframes.yml', methods=['POST'])
@swag_from('../docs/deleteframes.yml', methods=['DELETE'])
@swag_from('../docs/updateframes.yml', methods=['PUT'])
def frames():
    """
    Frames
    ~~~~~~

    Perform CRUD operations on the frames (protected route)

    Internally
    ----------
    API Key generated during login should be provided in header
    Payload: User_id

    POST:
        Reads the frame data from the request body and adds the frame

    GET:
        Nothing is needed in the request body
        It fetches all the frames from the database and sends the response

    PUT:
        Reads the frame_id and frame_data from the header
        Updates the frame_data of the particular id

    DELETE:
        Reads the frame_id from the header
        Deletes the frame_data from the database

    Returns
    -------
    make_response, status_code(int)
        The object with the data or message, and a corresponding HTTP status codes

    """

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
                responseObject = database.save_frame(auth_token, frame)
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
            frames_arr = database.get_frames(auth_token)
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
            if database.delete_frames(auth_token, frame_id):
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
            upd_frame = database.update_frames(auth_token, frame_id, frame_data)
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
