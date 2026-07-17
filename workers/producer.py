#!/usr/bin/env python3
"""
A producer is a user application that sends messages
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
from datetime import datetime

from queues import Queue


class Producer(Queue):
    def __init__(self):
        Queue.__init__(self, queue='work')


if __name__ == '__main__':
    NOW = datetime.now()
    p = Producer()
    for i in range(15):
        p.send(f'{i} {NOW} - Work - Hello World')
        print(f'{i} {NOW} - Work - Hello World sent')
    p.close()
