#!/usr/bin/env python
"""
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
import logging
import pika

logging.getLogger('pika').setLevel(logging.CRITICAL)

class Queue:
    def __init__(self, queue='queue', host='localhost', routing='route'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host))
        self.channel = self.connection.channel()
        self.routing = routing
        self.queue = queue

    def receive(self):
        self.channel.basic_consume(self.callback, queue=self.queue,
                                   no_ack=True)
        self.channel.start_consuming()

    def close(self):
            self.connection.close()