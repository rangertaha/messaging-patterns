

A Basic Example
=================

This example has three parts. The Producer, Queue, and the Consummer. The
producer sends produces messages places them in the queue. The


.. image:: ../images/basic.png



Producer
________

.. code-block:: python

    #!/usr/bin/env python
    from queue import Queue

    class Producer(Queue):
        def __init__(self):
            Queue.__init__(self, queue='basic')

    if __name__ == '__main__':
        p = Producer()
        p.send('Basic - Hello World')




.. code-block:: bash

    rangertaha@Ops:~/messaging-patterns/basic$ python producer.py
    0 2014-04-22 00:19:59.497745 - Basic - Hello World sent
    1 2014-04-22 00:19:59.497745 - Basic - Hello World sent
    2 2014-04-22 00:19:59.497745 - Basic - Hello World sent
    3 2014-04-22 00:19:59.497745 - Basic - Hello World sent
    4 2014-04-22 00:19:59.497745 - Basic - Hello World sent


























Consumer
________

.. code-block:: python

    #!/usr/bin/env python
    from queue import Queue

    class Consumer(Queue):
        def __init__(self):
            Queue.__init__(self, queue='basic')

        def callback(self, ch, method, properties, body):
            print 'Received: {0}'.format(body)

    if __name__ == '__main__':
        p = Consumer()
        p.receive(p.callback)


.. code-block:: bash

    rangertaha@Ops:~/messaging-patterns/basic$ python consumer.py
    0 2014-04-22 00:19:59.497745 - Basic - Hello World received
    1 2014-04-22 00:19:59.497745 - Basic - Hello World received
    2 2014-04-22 00:19:59.497745 - Basic - Hello World received
    3 2014-04-22 00:19:59.497745 - Basic - Hello World received
    4 2014-04-22 00:19:59.497745 - Basic - Hello World received













Queue
______

.. code-block:: python

    #!/usr/bin/env python
    import pika

    class Queue:
        def __init__(self, queue='queue', host='localhost', routing='route'):
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=host))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=queue)
            self.routing = routing
            self.queue = queue

        def send(self, msg):
            self.channel.basic_publish(exchange='',
                          routing_key=self.queue,
                          body=msg)

        def receive(self, callback):
            self.channel.basic_consume(callback,
                          queue=self.queue,
                          no_ack=True)
            self.channel.start_consuming()







