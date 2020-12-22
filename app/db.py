from config import Config, FirebaseConfig
from passlib.hash import pbkdf2_sha256
import pyrebase
import jwt
import datetime


def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, minutes=0),
            'iat': datetime.datetime.utcnow(),
            'id': user_id
        }
        return jwt.encode(
            payload,
            Config.SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, Config.SECRET_KEY)
        return payload['id']
    except jwt.ExpiredSignatureError:
        print('ERROR: Signature expired. Please log in again.')
        return None
    except jwt.InvalidTokenError:
        print('ERROR: Invalid token. Please log in again.')
        return None


class Db:
    @staticmethod
    def init_db():
        firebase = pyrebase.initialize_app(FirebaseConfig)
        db = firebase.database()
        if db:
            print(' * Database connected successfully')

        return db

    @staticmethod
    def add_participants(db, userDetails):
        try:
            user = {
                "name": userDetails["name"],
                "email": userDetails["email"],
                # storing the password as hash
                "password": pbkdf2_sha256.hash(userDetails["password"]),
                "frames": []
            }
            db.child('participants').push(user)
            print(' * Participant added to db')
            return True
        except Exception as e:
            print('ERROR:', e)
            return False

    @staticmethod
    def check_valid_details(db, userDetails):
        try:
            assert len(userDetails["name"]) > 0
            assert len(userDetails["email"]) > 0
            assert len(userDetails["password"]) > 6

            participants = db.child('participants').get().val()
            for user_id in participants:
                user = participants[user_id]
                if user and (user["email"] == userDetails["email"]):
                    print('ERROR: email already exists')
                    return False
            return True
        except Exception as e:
            print('ERROR:', e)
            return False

    @staticmethod
    def authorise_participants(db, userDetails):
        try:
            participants = db.child('participants').get().val()
            for user_id in participants:
                user = participants[user_id]
                if user and (user["email"] == userDetails["email"]) and (pbkdf2_sha256.verify(userDetails["password"], user["password"])):
                    return user_id
            return None
        except Exception as e:
            print('ERROR:', e)
            return None

    @staticmethod
    def get_token(db, user_id):
        try:
            token = encode_auth_token(user_id)
            return token.decode('UTF-8')
        except Exception as e:
            print('ERROR:', e)
            return None

    @staticmethod
    def save_frame(db, token, frame):
        try:
            user_id = decode_auth_token(token)
            if user_id!= None:
                db.child('participants').child(user_id).child('frames').push(frame)
                print('* Frame added successfully')
                return True
            else:
                print('ERROR: Token Value is None')
                return False
        except Exception as e:
            print('ERROR: ', e)
            return False

    @staticmethod
    def get_frames(db, token):
        try:
            user_id = decode_auth_token(token)
            frames = db.child('participants').child(
                user_id).child('frames').get().val()
            frame_arr = []
            if frames!= None:
                frame_arr = [frames[fid] for fid in frames]
            return frame_arr
        except Exception as e:
            print('ERROR: ', e)
            return None
