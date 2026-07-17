#!/usr/bin/env python3
"""
A consumer is a user application that receives messages.
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
from exchange import Exchange


class Consumer(Exchange):
    def __init__(self):
        Exchange.__init__(self, exchange='exchange-001',
                          exchange_type='fanout')
        self.bind()

    def bind(self):
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.channel.queue_bind(exchange=self.exchange,
                                queue=result.method.queue)
        self.queue = result.method.queue

    def callback(self, ch, method, properties, body):
        print(f'{body.decode()} received')


if __name__ == '__main__':
    p = Consumer()
    p.receive()
