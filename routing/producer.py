#!/usr/bin/env python
"""
"""
__author__ = 'rangertaha <rangertaha@gmail.com>'
import sys
from datetime import datetime
from exchange import Exchange


class Producer(Exchange):
    def __init__(self):
        Exchange.__init__(self, exchange='exchange_001', type='direct')
        self.routing=sys.argv[1]

    def send(self, msg):
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=self.routing,
                                   body=msg)

if __name__ == '__main__':
    NOW = datetime.now()
    p = Producer()
    for i in range(5):
        p.send('{0} {1} - Routing - {2}'.format(i, NOW, p.routing))
        print '{0} {1} - Routing - {2} sent'.format(i, NOW, p.routing)
    p.close()
