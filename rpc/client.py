#!/usr/bin/env python3
"""
An RPC client that sends a request with a correlation id and a reply queue,
then blocks until the matching response arrives.
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
import logging
import sys
import uuid

import pika

logging.getLogger('pika').setLevel(logging.CRITICAL)


class Client:
    def __init__(self, queue='rpc', host='localhost'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.queue = queue

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(queue=self.callback_queue,
                                   on_message_callback=self.on_response,
                                   auto_ack=True)
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, properties, body):
        if properties.correlation_id == self.corr_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events(time_limit=1)
        return int(self.response)

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    c = Client()
    print(f'fib({n}) requested')
    print(f'fib({n}) = {c.call(n)} received')
    c.close()
