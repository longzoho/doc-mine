from datetime import datetime

from firebase_admin import db


class UserConversation:
    def __init__(self, user_id: str, conversation_id: str, question_time: float, conversation_key: str):
        self.conversation_entity = db.reference(f'/users/{user_id}/conversations/{conversation_key}/{conversation_id}')
        self.entity = db.reference(f'/users/{user_id}/conversations/{conversation_key}/{conversation_id}/{question_time}')

    def create_if_not_exists(self):
        if not self.conversation_entity.get():
            self.conversation_entity.set({'create_time': int(datetime.now().timestamp()*1000)})
        if not self.entity.get():
            self.entity.set({})
        return self

    def add_question(self, question_text):
        self.entity.update({'question': question_text})

    def add_answer(self, answer: dict):
        self.entity.update({'answer': answer})
