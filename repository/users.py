from datetime import datetime

from firebase_admin import db


class Users:
    def __init__(self, uid):
        self.collection = db.reference("/users")
        self.entity = self.collection.child(uid)

    def create_if_not_exists(self):
        if not self.entity.get():
            self.entity.set({
                'documents': {},
                'create_time': datetime.now().timestamp()
            })
        return self
