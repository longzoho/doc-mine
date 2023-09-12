# wrap auth token verification in a decorator
from functools import wraps

from flask import request
from util import FirebaseUtils


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # get auth token
        auth_token = request.headers.get('Authorization')
        decoded_token = FirebaseUtils.verify_id_token(auth_token)
        uid = decoded_token['uid']
        kwargs['uid'] = uid
        return func(*args, **kwargs)

    return wrapper
