#!/usr/bin/env python3
"""
A producer is a user application that sends messages
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
from datetime import datetime

from exchange import Exchange


class Producer(Exchange):
    def __init__(self):
        Exchange.__init__(self, exchange='exchange-001',
                          exchange_type='fanout')

    def send(self, msg):
        self.channel.basic_publish(exchange=self.exchange, routing_key='',
                                   body=msg)


if __name__ == '__main__':
    NOW = datetime.now()
    p = Producer()
    for i in range(5):
        p.send(f'{i} {NOW} - Pub/Sub - Hello World')
        print(f'{i} {NOW} - Pub/Sub - Hello World sent')
    p.close()
