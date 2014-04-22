#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'

import pika
from queue import Queue

class Exchange(Queue):
    def __init__(self, exchange='exchange_001', type='direct'):
        Queue.__init__(self)
        self.channel.exchange_declare(exchange=exchange, type=type)
        self.exchange = exchange
        self.type = type