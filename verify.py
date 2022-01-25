
import jwt
from time import time

from app import app
def get_reset_token(username):
    return jwt.encode({'reset_password': username, 'exp': time() + 500}, key = app.config['SECRET_KEY'],algorithm='HS256')




def verify_reset_token(token):
    try:
        username = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
    except Exception as e:
        print(e)
        return
    return username