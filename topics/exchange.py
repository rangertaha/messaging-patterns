#!/usr/bin/env python3
"""
An exchange receives messages from producers and routes them to queues.
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
from queues import Queue


class Exchange(Queue):
    def __init__(self, exchange='exchange_002', exchange_type='topic'):
        Queue.__init__(self)
        self.channel.exchange_declare(exchange=exchange,
                                      exchange_type=exchange_type)
        self.exchange = exchange
        self.exchange_type = exchange_type
