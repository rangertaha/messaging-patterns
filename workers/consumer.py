#!/usr/bin/env python3
"""
A worker that processes one message at a time and acknowledges it when done.
Run several instances to spread the work across workers.
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
import time

from queues import Queue


class Consumer(Queue):
    def __init__(self):
        Queue.__init__(self, queue='work')

    def callback(self, ch, method, properties, body):
        print(f'{body.decode()} received')
        time.sleep(1)
        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    p = Consumer()
    p.receive()
