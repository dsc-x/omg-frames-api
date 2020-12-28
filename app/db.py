from config import FirebaseConfig
from passlib.hash import pbkdf2_sha256
from utils import Utils
import pyrebase


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
                "role": userDetails["role"],
                "organisation": userDetails["organisation"],
                # storing the password as hash
                "password": pbkdf2_sha256.hash(userDetails["password"]),
                "frames": []
            }
            db.child('participants').push(user)
            print(' * Participant added to db')
            return True
        except Exception as e:
            print('ERROR: <add_participants>', e)
            return False

    @staticmethod
    def check_valid_details(db, userDetails):
        try:
            assert len(userDetails["name"]) > 0
            assert len(userDetails["email"]) > 0
            assert len(userDetails["password"]) > 6

            participants = db.child('participants').get().val()
            if participants is None:
                # no participant data
                return True
            for user_id in participants:
                user = participants[user_id]
                if user and (user["email"] == userDetails["email"]):
                    print('ERROR: email already exists')
                    return False
            return True
        except Exception as e:
            print('ERROR: <check_valid_details>', e)
            return False

    @staticmethod
    def authorise_participants(db, userDetails):
        try:
            participants = db.child('participants').get().val()
            for user_id in participants:
                user = participants[user_id]
                if user and (user["email"] == userDetails["email"]) and (pbkdf2_sha256.verify(userDetails["password"], user["password"])):
                    return (user_id, user)
            return None
        except Exception as e:
            print('ERROR:', e)
            return None

    @staticmethod
    def get_token(db, user_id):
        try:
            token = Utils.encode_auth_token(user_id)
            return token.decode('UTF-8')
        except Exception as e:
            print('ERROR:', e)
            return None

    @staticmethod
    def save_frame(db, token, frame):
        try:
            user_id = Utils.decode_auth_token(token)
            if user_id is not None:
                frame_id = db.child('participants').child(user_id).child('frames').push(frame)
                frame_obj = {
                    "frame_data": frame,
                    "frame_id": frame_id["name"]
                }
                print('* Frame added successfully')
                return frame_obj
            else:
                print('ERROR: Token Value is None')
                return None
        except Exception as e:
            print('ERROR: ', e)
            return None

    @staticmethod
    def get_frames(db, token):
        try:
            user_id = Utils.decode_auth_token(token)
            if user_id is not None:
                frames = db.child('participants').child(user_id).child('frames').get().val()
                frame_arr = []
                if frames is not None:
                    frame_arr = [{"frame_id": fid, "frame_data": frames[fid]} for fid in frames]
                return frame_arr
            else:
                print('ERROR: Token Value is None')
                return None
        except Exception as e:
            print('ERROR: ', e)
            return None

    @staticmethod
    def delete_frames(db, token, frame_id):
        try:
            user_id = Utils.decode_auth_token(token)
            if user_id is not None:
                db.child('participants').child(user_id).child('frames').child(frame_id).remove()
                return True
            else:
                print('ERROR: Token Value is None')
                return False
        except Exception as e:
            print('ERROR: ', e)
            return False

    @staticmethod
    def update_frames(db, token, frame_id, frame_data):
        user_id = Utils.decode_auth_token(token)
        if user_id is not None:
            db.child('participants').child(user_id).child('frames').child(frame_id).remove()
            upd_frame_id = db.child('participants').child(user_id).child('frames').push(frame_data)
            frame = {"frame_id": upd_frame_id['name'], "frame_data": frame_data}
            return frame
        else:
            print('ERROR: Token Value is None')
            return None

    @staticmethod
    def check_email_address(db, email):
        participants = db.child('participants').get().val()
        if participants is None:
            # No records found
            return None
        else:
            for user_id in participants:
                user = participants[user_id]
                if user and (user["email"] == email):
                    return user_id
            return None

    @staticmethod
    def change_password(db, user_id, password):
        user_details = db.child('participants').child(user_id).get().val()
        user_details['password'] = pbkdf2_sha256.hash(password)
        db.child('participants').child(user_id).update(user_details)
