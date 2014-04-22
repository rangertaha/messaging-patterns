#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
A queue is a buffer that stores messages
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
        self.channel.queue_declare(queue=queue)
        self.routing = routing
        self.queue = queue

    def send(self, msg):
        self.channel.basic_publish(exchange='',
                      routing_key=self.queue,
                      body=msg)

    def receive(self):
        self.channel.basic_consume(self.callback,
                      queue=self.queue,
                      no_ack=True)
        self.channel.start_consuming()

    def close(self):
        self.connection.close()