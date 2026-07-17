#!/usr/bin/env python3
"""
A producer is a user application that sends messages
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
import sys
from datetime import datetime

from exchange import Exchange


class Producer(Exchange):
    def __init__(self, topic):
        Exchange.__init__(self, exchange='exchange_002',
                          exchange_type='topic')
        self.topic = topic

    def send(self, msg):
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=self.topic,
                                   body=msg)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(f'usage: {sys.argv[0]} <topic>   (ex: kern.critical)')
    NOW = datetime.now()
    p = Producer(sys.argv[1])
    for i in range(5):
        p.send(f'{i} {NOW} - Topics - {p.topic}')
        print(f'{i} {NOW} - Topics - {p.topic} sent')
    p.close()
