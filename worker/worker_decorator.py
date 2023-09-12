from functools import wraps

import pika


def document_convert_channel(func, key='msg_channel'):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # get auth token
        _connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost", port=5672))
        channel = _connection.channel()
        channel.exchange_declare(exchange="document_convert_process_exchange", exchange_type="direct")
        channel.queue_declare(queue="document_convert_process_queue", durable=True)
        kwargs[key] = channel
        result = func(*args, **kwargs)
        _connection.close()
        return result

    return wrapper


def conversation_asking_channel(func, key='msg_channel'):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # get auth token
        _connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost", port=5672))
        channel = _connection.channel()
        channel.exchange_declare(exchange="ai_search_process_exchange", exchange_type="direct")
        channel.queue_declare(queue="ai_search_process_queue", durable=True)
        kwargs[key] = channel
        result = func(*args, **kwargs)
        _connection.close()
        return result

    return wrapper
