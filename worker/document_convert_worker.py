import json
from functools import wraps

import pika
from dotenv import load_dotenv

from data_types import DocumentData
from util import FirebaseUtils
from workflow.convert_document_flow import convert_documents_flow
from workflow.message_channel import RoutingKeys, use_message_channel


def document_save_consumer(ch, method, properties, body):
    print(" [x] Start call document_save_consumer")
    json_body = json.loads(body)
    message_type = method.routing_key
    if message_type == RoutingKeys.convert_document_topic:
        document_data = list(map(lambda x: DocumentData(**x), json_body.get("document_data")))
        user_id = json_body.get("user_id")
        convert_documents_flow(document_data=document_data, user_id=user_id)
    else:
        print(" [x] Received unknown message type")


def start_document_convert_worker():
    # Create a connection to RabbitMQ.
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, heartbeat=60 * 30))
    # Query processing channel.
    query_processing_channel = connection.channel()

    # Set the prefetch count for the query processing channel to 1.
    query_processing_channel.basic_qos(prefetch_count=4, global_qos=False)

    # Set exchange
    query_processing_channel.exchange_declare(exchange="document_convert_process_exchange", exchange_type="direct")

    query_processing_channel.queue_bind(exchange="document_convert_process_exchange",
                                        queue="document_convert_process_queue",
                                        routing_key=RoutingKeys.convert_document_topic)

    # Bind the consumer to the queue.
    query_processing_channel.queue_declare(queue="document_convert_process_queue", durable=True)
    query_processing_channel.basic_consume(queue="document_convert_process_queue",
                                           on_message_callback=document_save_consumer,
                                           auto_ack=True)

    # Start consuming messages.
    query_processing_channel.start_consuming()


if __name__ == '__main__':
    load_dotenv()
    FirebaseUtils.firebase_initialize()
    start_document_convert_worker()
