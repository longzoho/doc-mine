# wrap auth token verification in a decorator
from functools import wraps

import pika


class RoutingKeys(str):
    summary_document_topic = "summary_document_topic"
    conversation_asking_topic = "conversation_asking_topic"
    convert_document_topic = "convert_document_topic"
    embed_document_topic = "embed_document_topic"


def use_message_channel(func, queue_name: str):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # get auth token
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost", port=5672))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        kwargs['msg_channel'] = channel
        result = func(*args, **kwargs)
        connection.close()
        return result

    return wrapper
