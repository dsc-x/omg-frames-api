import os


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(24)


FirebaseConfig = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": "flask-auth-999fd.firebaseapp.com",
    "projectId": "flask-auth-999fd",
    "databaseURL": "https://flask-auth-999fd-default-rtdb.firebaseio.com/",
    "storageBucket": "flask-auth-999fd.appspot.com",
    "messagingSenderId": "76879405261",
    "appId": "1:76879405261:web:ed54378b0ed9289f300984"
}