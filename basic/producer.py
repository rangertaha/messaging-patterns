#!/usr/bin/env python
"""
A producer is a user application that sends messages
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
from datetime import datetime
from queue import Queue


class Producer(Queue):
    """
    """
    def __init__(self):
        Queue.__init__(self, queue='basic')

if __name__ == '__main__':
    NOW = datetime.now()
    p = Producer()
    for i in range(5):
        p.send('{0} {1} - Basic - Hello World'.format(i, NOW))
        print '{0} {1} - Basic - Hello World sent'.format(i, NOW)
    p.close()
