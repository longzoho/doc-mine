import json
from functools import wraps

import pika
from dotenv import load_dotenv

from util import FirebaseUtils
from workflow.conversation_asking_flow import conversation_asking_flow
from workflow.document_summary_flow import summary_document_flow
from workflow.embed_document_flow import embed_document_flow
from workflow.message_channel import RoutingKeys, use_message_channel


def question_answer_consumer(ch, method, properties, body):
    print(" [x] Start call question_answer_consumer")
    json_body = json.loads(body)
    message_type = method.routing_key
    if message_type == RoutingKeys.summary_document_topic:
        hash_name = json_body.get("hash_name")
        user_id = json_body.get("user_id")
        summary_document_flow(hash_name=hash_name, user_id=user_id)
    elif message_type == RoutingKeys.conversation_asking_topic:
        conversation_key = json_body.get("conversation_key")
        user_id = json_body.get("user_id")
        conversation_id = json_body.get("conversation_id")
        question_time = json_body.get("question_time")
        question_text = json_body.get("question_text")
        conversation_asking_flow(conversation_key=conversation_key, user_id=user_id, conversation_id=conversation_id,
                                 question_text=question_text, question_time=question_time)
    elif message_type == RoutingKeys.embed_document_topic:
        hash_name = json_body.get("hash_name")
        user_id = json_body.get("user_id")
        embed_document_flow(hash_name=hash_name, user_id=user_id)

    else:
        print(" [x] Received unknown message type")


def start_conversation_asking_worker():
    # Create a connection to RabbitMQ.
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672))
    # Query processing channel.
    query_processing_channel = connection.channel()

    # Set the prefetch count for the query processing channel to 1.
    query_processing_channel.basic_qos(prefetch_count=1, global_qos=False)

    # Set the exchange for the query processing channel.
    query_processing_channel.exchange_declare(exchange="ai_search_process_exchange", exchange_type="direct")
    query_processing_channel.exchange_declare(exchange="document_embed_process_exchange", exchange_type="direct")

    # Bind the consumer to the queue.
    query_processing_channel.queue_declare(queue="ai_search_process_queue", durable=True)
    query_processing_channel.queue_bind(exchange="ai_search_process_exchange", queue="ai_search_process_queue",
                                        routing_key=RoutingKeys.conversation_asking_topic)
    query_processing_channel.queue_bind(exchange="ai_search_process_exchange", queue="ai_search_process_queue",
                                        routing_key=RoutingKeys.summary_document_topic)
    query_processing_channel.queue_bind(exchange="document_embed_process_exchange", queue="ai_search_process_queue",
                                        routing_key=RoutingKeys.embed_document_topic)
    query_processing_channel.basic_consume(queue="ai_search_process_queue",
                                           on_message_callback=question_answer_consumer,
                                           auto_ack=True)
    # Start consuming messages.
    query_processing_channel.start_consuming()


if __name__ == '__main__':
    load_dotenv()
    FirebaseUtils.firebase_initialize()
    start_conversation_asking_worker()
