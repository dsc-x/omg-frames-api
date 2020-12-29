from config import FirebaseConfig
from passlib.hash import pbkdf2_sha256
from utils import Utils
import pyrebase


class Db:

    db = None

    def __init__(self):
        """Initilises the database 

        For more information of pyrebase https://github.com/thisbejim/Pyrebase
        """
        firebase = pyrebase.initialize_app(FirebaseConfig)
        self.db = firebase.database()
        if self.db:
            print(' * Database connected successfully')

    def add_participants(self, userDetails):
        """Adds participants to the database

        Args:
            userDetails (dict): Contains all the user related information

        Returns:
            bool: True if the data was inserted into database, False otherwise
        """

        try:
            # userDetails.get() is used to avoid KeyError caused due to failed dictionary key lookup.
            user = {
                "name": userDetails.get('name', ''),
                "email": userDetails.get('email', ''),
                "role": userDetails.get('role', ''),
                "organisation": userDetails.get('organisation', ''),
                # storing the password as hash
                "password": pbkdf2_sha256.hash(userDetails.get('password', '')),
                "frames": []
            }
            self.db.child('participants').push(user)
            return True
        except Exception as e:
            print('ERROR: <add_participants>', str(e))
            return False

    def check_valid_details(self, userDetails):
        """Checks if the details provided are valid and unique

        Args:
            userDetails (dict): Contains all the user information like name, email, role, org

        Returns:
            bool: True is details are valid, False otherwise
        """

        try:
            assert len(userDetails["name"]) > 0
            assert len(userDetails["email"]) > 0
            assert len(userDetails["password"]) > 6

            participants = self.db.child('participants').get().val()
            if participants is None:
                # when there is no data in the database
                return True
            for user_id in participants:
                user = participants[user_id]
                if user and (user["email"] == userDetails["email"]):
                    print('ERROR: email already exists')
                    return False
            return True
        except Exception as e:
            print('ERROR: <check_valid_details>', str(e))
            return False

    def authorise_participants(self, userDetails):
        """Checks if the email and password are in the database

        Args:
            userDetails (dict): Contains email and password

        Returns:
            (str, dict): User data key,User record
        """

        try:
            participants = self.db.child('participants').get().val()
            for user_id in participants:
                user = participants[user_id]
                #for password we have to verify the hash
                if user and (user["email"] == userDetails["email"]) and (pbkdf2_sha256.verify(userDetails["password"], user["password"])):
                    return (user_id, user)
            return None
        except Exception as e:
            print('ERROR:', str(e))
            return None

    # def get_token(self, user_id):
    #     try:
    #         token = Utils.encode_auth_token(user_id)
    #         return token.decode('UTF-8')
    #     except Exception as e:
    #         print('ERROR:', e)
    #         return None

    def save_frame(self, token, frame):
        """Save frames of the user

        Args:
            token (str): JWT token passed with the header, containing the user id as payload
            frame (str): Base64 encoded data of the frame

        Returns:
            dict of str: str : Contains the frame_id generated and the data of the frame
        """

        try:
            user_id = Utils.decode_auth_token(token)
            if user_id is not None:
                frame_id = self.db.child('participants').child(user_id).child('frames').push(frame)
                frame_obj = {
                    "frame_data": frame,
                    "frame_id": frame_id["name"]
                }
                return frame_obj
            else:
                print('ERROR: Token Value is None')
                return None
        except Exception as e:
            print('ERROR: ', str(e))
            return None

    def get_frames(self, token):
        """Get all the frames

        Args:
            token (str): JWT token passed with the header, containing the user id as payload

        Returns:
            List[dict]: array of frame objects
        """

        try:
            user_id = Utils.decode_auth_token(token)
            if user_id is not None:
                frames = self.db.child('participants').child(user_id).child('frames').get().val()
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

    def delete_frames(self, token, frame_id):
        """Deletes the frame

        Args:
            token (str): JWT token passed with the header, containing the user id as payload
            frame_id (str): frame id to be deleted

        Returns:
            bool: True is success, else False
        """       

        try:
            user_id = Utils.decode_auth_token(token)
            if user_id is not None:
                self.db.child('participants').child(user_id).child('frames').child(frame_id).remove()
                return True
            else:
                print('ERROR: Token Value is None')
                return False
        except Exception as e:
            print('ERROR: ', e)
            return False

    def update_frames(self, token, frame_id, frame_data):
        """update frames of the user

        Args:
            token (str): JWT token passed with the header, containing the user id as payload
            frame_id (str): frame id to be updated
            frame_data (str): base64 encoded data of the new frame

        Returns:
            dict : Contains the frame_id generated and the data of the frame
        """

        user_id = Utils.decode_auth_token(token)
        if user_id is not None:
            self.db.child('participants').child(user_id).child('frames').child(frame_id).remove()
            upd_frame_id = self.db.child('participants').child(user_id).child('frames').push(frame_data)
            frame = {"frame_id": upd_frame_id['name'], "frame_data": frame_data}
            return frame
        else:
            print('ERROR: Token Value is None')
            return None

    def check_email_address(self, email):
        """Check if the email address exists in the database
        
        Args:
            email: email of the user to be checked
        Returns:
            str: user_id of the corresponding email
        """

        participants = self.db.child('participants').get().val()
        if participants is None:
            # No records found
            return None
        else:
            for user_id in participants:
                user = participants[user_id]
                if user and (user["email"] == email):
                    return user_id
            return None

    def change_password(self, user_id, password):
        """Change the password of the user in the database

        Args:
            user_id (string): id of the user whose password has to be updated
            password (string): new password of the user
        """
        user_details = self.db.child('participants').child(user_id).get().val()
        user_details['password'] = pbkdf2_sha256.hash(password)
        self.db.child('participants').child(user_id).update(user_details)
