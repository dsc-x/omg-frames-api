from config import Config, FirebaseConfig
from passlib.hash import pbkdf2_sha256
import pyrebase
import jwt 
import datetime

def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=10),
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
                "name":userDetails["name"],
                "email":userDetails["email"],
                "password":pbkdf2_sha256.hash(userDetails["password"]), #storing the password as hash
                "frames":[]
            }
            db.child('participants').push(user)
            print(' * Participant added to db')
            return True
        except Exception as e:
            print('ERROR: add_participants', e)
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
            print('ERROR: authorise_participants', e)

    @staticmethod
    def get_token(db, user_id):
        try:
            token=encode_auth_token(user_id)
            return token.decode('UTF-8')
        except Exception as e:
            print('ERROR: get_token', e)
            return None