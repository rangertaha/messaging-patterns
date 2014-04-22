#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
A consumer is a user application that receives messages.
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
from queue import Queue


class Consumer(Queue):
    """

    """
    def __init__(self):
        Queue.__init__(self, queue='basic')

    def callback(self, ch, method, properties, body):
        print '{0} received '.format(body)

if __name__ == '__main__':
    p = Consumer()
    p.receive(p.callback)
