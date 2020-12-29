import jwt
import datetime
from config import Config
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Message
from flask import render_template


class Utils:
    """Utility functions used in the app
    """
    @staticmethod
    def encode_auth_token(user_id):
        """JWT encodes a payload

        It has an expiry of 1 day
        Payload is the user_id provided in the Arg
        Secret key is the app secret key

        Args:
            user_id (str): user_id which will be stored in the payload

        Returns:
            str: UTF-8 jwt token
        """
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
            ).decode('UTF-8')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """JWT decodes a token

        Args:
            auth_token (str): JWT token to be decoded

        Returns:
            str : the payload data stored
        """
        try:
            payload = jwt.decode(auth_token, Config.SECRET_KEY)
            return payload['id']
        except jwt.ExpiredSignatureError:
            print('ERROR: Signature expired. Please log in again.')
            return None
        except jwt.InvalidTokenError:
            print('ERROR: Invalid token. Please log in again.')
            return None

    @staticmethod
    def get_reset_token(user_id):
        """Generates a reset token

        This is used in the Reset password mail
        User_id is the payload in the token
        It has an expiry of 1 day

        Args:
            user_id (str): [description]

        Returns:
            str: Token generated
        """
        expires_sec=int(datetime.timedelta(days=1).total_seconds())
        #Serializer function takes time in secs
        s = Serializer(Config.SECRET_KEY, expires_sec)
                
        return s.dumps({'user_id': user_id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """To verify the token

        Args:
            token (str): token to be verified

        Returns:
            str: payload data, user_id in this case
        """
        s = Serializer(Config.SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except Exception as e:
            print('ERROR: ', str(e))
            return None
        return user_id

    @staticmethod
    def send_reset_password_mail(mail, link, recipient_addr):
        """Send the reset password mail

        Args:
            mail (Mail): Mail object initialized in __init__.py
            link (str): URL link to be embedded in the mail
            recipient_addr (str): Email of the recipient
        """
        msg = Message("Reset password for IWasAt", sender='noreply@iwasat.events', recipients=[recipient_addr])
        msg.body = 'You or someone else has requested that a new password be generated for your account. If you made this request, then please follow this link:' + link
        msg.html = render_template('reset-password.html', link=link)
        mail.send(msg)
