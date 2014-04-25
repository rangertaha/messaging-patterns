#!/usr/bin/env python
"""
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
from datetime import datetime
from exchange import Exchange


class Producer(Exchange):
    def __init__(self):
        Exchange.__init__(self, exchange='exchange-001', type='fanout')

    def send(self, msg):
        self.channel.basic_publish(exchange=self.exchange, routing_key='',
                                   body=msg)

if __name__ == '__main__':
    NOW = datetime.now()
    p = Producer()
    for i in range(5):
        p.send('{0} {1} - Pub/Sub - Hello World'.format(i, NOW))
        print '{0} {1} - Pub/Sub - Hello World sent'.format(i, NOW)
    p.close()
