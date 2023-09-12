import json
import uuid
from datetime import datetime

from flask import request

from decorator import auth_required
from repository.user_conversation import UserConversation
from worker.worker_decorator import conversation_asking_channel
from workflow.message_channel import RoutingKeys


@auth_required
@conversation_asking_channel
def ask(uid, msg_channel):
    # get hash_name and query from request body
    question_text, conversation_key = request.json.get('question_text'), request.json.get('conversation_key')
    conversation_id = request.json.get('conversation_id') or uuid.uuid4().hex
    if question_text is None or conversation_key is None:
        return {'message': 'query and hash_name are required'}, 400
    question_time = int(datetime.now().timestamp() * 1000)
    entity = UserConversation(user_id=uid, conversation_id=conversation_id,
                              question_time=question_time, conversation_key=conversation_key).create_if_not_exists()
    entity.add_question(question_text=question_text)
    body = json.dumps({'user_id': uid, 'conversation_key': conversation_key,
                       'conversation_id': conversation_id,
                       'question_text': question_text,
                       'question_time': question_time})
    print(body)
    msg_channel.basic_publish(exchange="ai_search_process_exchange", routing_key=RoutingKeys.conversation_asking_topic,
                              body=body)
    return {'conversation_id': conversation_id}, 200
