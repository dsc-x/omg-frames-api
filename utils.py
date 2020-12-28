import jwt
import datetime
from config import Config
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Message
from flask import render_template


class Utils:
    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def get_reset_token(user_id, expires_sec=1800):
        s = Serializer(Config.SECRET_KEY, expires_sec)
        return s.dumps({'user_id': user_id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except Exception as e:
            print('ERROR: ', str(e))
            return None
        return user_id

    @staticmethod
    def send_reset_password_mail(mail, link, recipient_addr):
        msg = Message("Send Mail Tutorial!",
                      sender=Config.SENDER_ADDR,
                      recipients=[recipient_addr])
        msg.subject = 'Reset password for IWasAtEvents'
        msg.body = 'You or someone else has requested that a new password be generated for your account. If you made this request, then please follow this link:' + link
        msg.html = render_template('reset-password.html', link=link)
        mail.send(msg)
