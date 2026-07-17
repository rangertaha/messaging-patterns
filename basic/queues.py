#!/usr/bin/env python3
"""
A queue is a buffer that stores messages
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
import logging

import pika

logging.getLogger('pika').setLevel(logging.CRITICAL)


class Queue:
    def __init__(self, queue='queue', host='localhost'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.queue = queue

    def send(self, msg):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue,
                                   body=msg)

    def receive(self):
        self.channel.basic_consume(queue=self.queue,
                                   on_message_callback=self.callback,
                                   auto_ack=True)
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
