from firebase_admin import initialize_app, db, auth
import os
from functools import lru_cache


class FirebaseUtils:
    @classmethod
    @lru_cache(maxsize=1)
    def firebase_initialize(cls):
        return initialize_app(options={
            'databaseURL': os.getenv('FIREBASE_DATABASE_URL'),
        })

    @classmethod
    def get_collection_users(cls):
        return db.reference("/users")

    @classmethod
    def verify_id_token(cls, auth_token):
        return auth.verify_id_token(auth_token)
