#!/usr/bin/env python
"""
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
import time
from exchange import Exchange


class Consumer(Exchange):
    def __init__(self):
        Exchange.__init__(self, exchange='exchange-001', type='fanout')
        self.bind()

    def bind(self):
        result = self.channel.queue_declare(exclusive=True)
        self.channel.queue_bind(exchange=self.exchange, queue=result.method.queue)
        self.queue = result.method.queue

    def callback(self, ch, method, properties, body):
        print '{0} received '.format(body)
        #time.sleep(5)

if __name__ == '__main__':
    p = Consumer()
    p.receive()
