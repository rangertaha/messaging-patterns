#!/usr/bin/env python3
"""
A consumer is a user application that receives messages.
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
from queues import Queue


class Consumer(Queue):
    def __init__(self):
        Queue.__init__(self, queue='basic')

    def callback(self, ch, method, properties, body):
        print(f'{body.decode()} received')


if __name__ == '__main__':
    p = Consumer()
    p.receive()
