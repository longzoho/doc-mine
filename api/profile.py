import logging
import uuid
from threading import Thread

from flask import request

from decorator import auth_required
from repository.profiles import Profiles
from workflow.embed_profile_flow import embed_profile_flow

logger = logging.getLogger(__name__)


@auth_required
def create(uid):
    if request.data:
        json_data = request.get_json()
        name, description, hash_names = json_data.get('name'), json_data.get('description'), json_data.get('hash_names')
        if name is None or description is None or hash_names is None:
            return {'message': 'name, description and hash_names are required'}, 400
    new_profile_id = uuid.uuid4().hex
    Profiles(user_id=uid, profile_id=new_profile_id).create_if_not_exists(name=name, description=description,
                                                                          document_hash_names=hash_names)
    thread = Thread(target=lambda: embed_profile_flow(user_id=uid, profile_id=new_profile_id))
    thread.start()
    return {'message': 'success', 'profile_id': new_profile_id}, 200
