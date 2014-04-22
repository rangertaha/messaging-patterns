#!/usr/bin/env python
#-*- coding:utf-8 -*-
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
    """
    def publish(self, msg):
        self.channel.queue_declare(queue=self.queue)
        self.channel.basic_publish(exchange=self.exchange, routing_key=self
        .queue, body=msg)

    def bind(self):
        result = self.channel.queue_declare(exclusive=True)
        queue = result.method.queue
        self.channel.queue_bind(exchange=self.exchange, queue=queue)
    """
    def receive(self, callback):
        self.channel.basic_consume(callback, queue=self.queue, no_ack=True)
        self.channel.start_consuming()

    def close(self):
            self.connection.close()