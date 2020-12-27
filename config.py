import os


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(24)


FirebaseConfig = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": "dscxframes.firebaseapp.com",
    "databaseURL": "https://dscxframes-default-rtdb.firebaseio.com",
    "projectId": "dscxframes",
    "storageBucket": "dscxframes.appspot.com",
    "messagingSenderId": "21222617342",
    "appId": "1:21222617342:web:f03af782ee33832a39f5af",
    "measurementId": "G-Y797P25ZN9"
}