#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'

import pika


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

    def receive(self, callback):
        self.channel.basic_consume(callback,
                      queue=self.queue,
                      no_ack=True)
        self.channel.start_consuming()

    def close(self):
            self.connection.close()