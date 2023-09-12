import argparse
import json
import time

import pika
from prefect import task, flow

from data_types import DocumentData
from workflow.message_channel import RoutingKeys

body = {'user_id': 'CSDbQdORdoV18WfCa2r9zFwfC552', 'document_data': [
    {'name': 'electronic-commerce.pdf',
     'hash_name': 'c13ec2d7b03d99599ab05b91052aae6682d137c3318b9db2efeaa84309b98a51__pdf'}]}


def printout(document_data: list[DocumentData]):
    print(str(document_data))


@task
def task_1(n):
    print(f'task_1 {n}')
    time.sleep(.1)
    return n


@task
def task_2(n):
    print(f'task_2 {n}')
    time.sleep(.1)


@task
def task_3():
    print('task_3')
    time.sleep(.1)


@flow
def my_flow():
    list_n = list(['a', 'b', 'c'])
    x = task_1.map(n=list_n)

    # task 2 will wait for task_1 to complete
    y = task_2.map(n=x)

    task_3.submit(wait_for=[y])


if __name__ == '__main__':
    # my_flow()
    _connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672))
    channel = _connection.channel()
    channel.queue_declare(queue="document_convert_process_queue", durable=True)
    channel.queue_bind(exchange="document_convert_process_exchange", queue="document_convert_process_queue")
    channel.exchange_declare(exchange="document_convert_process_exchange", exchange_type="direct")
    channel.basic_publish(exchange="document_convert_process_exchange", routing_key=RoutingKeys.convert_document_topic,
                          body=bytes(json.dumps(body), encoding="utf-8"))
    channel.close()
