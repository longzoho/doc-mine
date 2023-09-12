import json
from datetime import datetime

from firebase_admin import db

from data_types import FileStatus

available_status = [FileStatus.CONTENT_SAVED, FileStatus.DOCUMENT_SAVED, FileStatus.EMBED_SAVED, FileStatus.ERROR]


class Documents:
    def __init__(self, hash_name):
        self.collection = db.reference("/documents")
        self.entity = self.collection.child(hash_name)

    def create_if_not_exists(self, status: FileStatus):
        data = self.entity.get()
        if not data:
            self.entity.set({"status": status, 'create_time': datetime.now().timestamp()})

    def update_status(self, status: FileStatus):
        _entity = self.entity.get()
        _entity = _entity or {}
        _status = _entity.get("status")
        if _status is None:
            self.entity.set({**_entity, "status": status})
        else:
            # update if index of status in available_status is greater than index of _status in available_status
            if available_status.index(status) > available_status.index(str(_status)):
                self.entity.set({**_entity, "status": status})

    def update_summary(self, summary: str):
        data = self.entity.get()
        if data:
            data = json.loads(json.dumps(data))
            self.entity.update({**data, 'summary': summary})
