import json
from datetime import datetime

from firebase_admin import db

from data_types import DocumentData, FileStatus, ProfileData, ProfileStatus
from util.utils import object_to_dict

available_status = [FileStatus.CONTENT_SAVED, FileStatus.DOCUMENT_SAVED, FileStatus.EMBED_SAVED, FileStatus.ERROR]


class Profiles:
    def __init__(self, user_id: str, profile_id: str):
        self.entity = db.reference(f'/users/{user_id}/profiles/{profile_id}')
        self.user_document_entity = db.reference(f'/users/{user_id}/documents')
        self.profile_id = profile_id

    def create_if_not_exists(self, name: str, description: str, document_hash_names: list[str]):
        if not self.entity.get():
            # get user_documents dict from user_documents_entity
            user_documents = object_to_dict(self.user_document_entity.get())
            documents = {}
            for hash_name in document_hash_names:
                if hash_name in user_documents:
                    documents[hash_name] = user_documents[hash_name]
            new_profile = {'name': name, 'description': description, 'documents': documents,
                           'create_time': datetime.now().timestamp(), 'status': ProfileStatus.INIT}
            self.entity.set(new_profile)
        return self

    def update_status(self, status: ProfileStatus):
        data = self.entity.get()
        if data:
            data = json.loads(json.dumps(data))
            self.entity.update({**data, 'status': status})

    def get_profile(self):
        return self.entity.get()
