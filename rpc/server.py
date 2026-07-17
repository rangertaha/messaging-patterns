#!/usr/bin/env python3
"""
An RPC server that listens for requests on a queue, computes the result,
and publishes it back to the client's reply queue.
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
import logging

import pika

logging.getLogger('pika').setLevel(logging.CRITICAL)


class Server:
    def __init__(self, queue='rpc', host='localhost'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.queue = queue

    @staticmethod
    def fib(n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    def callback(self, ch, method, properties, body):
        n = int(body)
        print(f'fib({n}) requested')
        response = self.fib(n)
        ch.basic_publish(exchange='',
                         routing_key=properties.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=properties.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def serve(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue,
                                   on_message_callback=self.callback)
        print('Awaiting RPC requests. Press CTRL+C to exit.')
        self.channel.start_consuming()


if __name__ == '__main__':
    s = Server()
    s.serve()
