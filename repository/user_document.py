import json
from datetime import datetime

from firebase_admin import db


class UserDocument:
    def __init__(self, user_id, hash_name):
        self.entity = db.reference(f'/users/{user_id}/documents/{hash_name}')

    def create_if_not_exists(self, name, status):
        if not self.entity.get():
            self.entity.set({'status': status, 'name': name, 'create_time': datetime.now().timestamp()})
        return self

    def update_status(self, status):
        data = self.entity.get()
        if data:
            data = json.loads(json.dumps(data))
            self.entity.update({**data, 'status': status})

    def update_summary(self, summary: str):
        data = self.entity.get()
        if data:
            data = json.loads(json.dumps(data))
            self.entity.update({**data, 'summary': summary})


class UserDocumentData:
    def __init__(self, name, status):
        self.name = name
        self.status = status

    def to_dict(self):
        return {
            'name': self.name,
            'status': self.status
        }
