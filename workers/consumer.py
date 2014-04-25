#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
import time
from queue import Queue


class Consumer(Queue):
    """
    """
    def __init__(self):
        Queue.__init__(self, queue='work')

    def callback(self, ch, method, properties, body):
        print '{0} received '.format(body)
        time.sleep(5)

if __name__ == '__main__':
    p = Consumer()
    p.receive(p.callback)
