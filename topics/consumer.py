#!/usr/bin/env python3
"""
A consumer is a user application that receives messages.
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
import sys

from exchange import Exchange


class Consumer(Exchange):
    def __init__(self, patterns):
        Exchange.__init__(self, exchange='exchange_002',
                          exchange_type='topic')
        self.patterns = patterns
        self.bind()

    def bind(self):
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue = result.method.queue
        for pattern in self.patterns:
            self.channel.queue_bind(exchange=self.exchange,
                                    queue=self.queue,
                                    routing_key=pattern)

    def callback(self, ch, method, properties, body):
        print(f'{body.decode()} received')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(f'usage: {sys.argv[0]} <pattern>...   (ex: "kern.*" "*.critical" "#")')
    p = Consumer(sys.argv[1:])
    p.receive()
