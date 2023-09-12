from workflow.message_channel import message_channel, RoutingKeys


@message_channel
def ask(msg_channel):
    msg_channel.basic_publish(exchange="ai-query", routing_key=RoutingKeys.conversation_asking_topic,
                              body='{"user_id": "CSDbQdORdoV18WfCa2r9zFwfC552", "conversation_key": "01b9cc0ebc882800b8ec641d8c29ee44bd620bb15a54ca71a69591136cb7081b__pdf", "conversation_id": "8a4cc539a0c348a7ba4fb74408fc751e", "question_text": "Are Tom fall in love", "question_time": 1694325000185}')


if __name__ == '__main__':
    ask()
