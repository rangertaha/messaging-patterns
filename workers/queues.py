#!/usr/bin/env python3
"""
A durable work queue that distributes messages across multiple workers.
Messages are persisted and acknowledged so no work is lost if a worker dies.
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
import logging

import pika

logging.getLogger('pika').setLevel(logging.CRITICAL)


class Queue:
    def __init__(self, queue='work', host='localhost'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue, durable=True)
        self.queue = queue

    def send(self, msg):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            body=msg,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent))

    def receive(self):
        # Only hand a worker one message at a time; the next message is
        # dispatched after the previous one is acknowledged.
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue,
                                   on_message_callback=self.callback)
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
