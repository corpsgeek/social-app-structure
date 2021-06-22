import os
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.models import db


# adding token confirmation to newly registered user
def token_generator(user):
    s = Serializer(os.environ.get('SECRET_KEY'), expires_in=3600)
    token = s.dumps({'confirm': user.id})

    return token


# confirm the token
def token_confirmation(user, token):
    s = Serializer(os.environ.get('SECRET_KEY'))
    try:
        data = s.loads(token)
    except:
        return False
    if data.get('confirm') != user.id:
        return False
    elif data.get('confirm') == user.id:
        user.confirmed = True
        db.session.add(user)
        return True
