

Routing
=======





.. image:: ../images/routing.png











Producer
________

The producer sends messages to the exchange.


.. code-block:: python

    #!/usr/bin/env python
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



.. code-block:: bash

    rangertaha@Coder:~/messaging-patterns/routing$ python producer.py blue
    0 2014-04-22 12:08:08.657679 - Routing - blue sent
    1 2014-04-22 12:08:08.657679 - Routing - blue sent
    2 2014-04-22 12:08:08.657679 - Routing - blue sent
    3 2014-04-22 12:08:08.657679 - Routing - blue sent
    4 2014-04-22 12:08:08.657679 - Routing - blue sent
    rangertaha@Coder:~/messaging-patterns/routing$ python producer.py red
    0 2014-04-22 12:08:12.715046 - Routing - red sent
    1 2014-04-22 12:08:12.715046 - Routing - red sent
    2 2014-04-22 12:08:12.715046 - Routing - red sent
    3 2014-04-22 12:08:12.715046 - Routing - red sent
    4 2014-04-22 12:08:12.715046 - Routing - red sent
    rangertaha@Coder:~/messaging-patterns/routing$ python producer.py green
    0 2014-04-22 12:08:19.934197 - Routing - green sent
    1 2014-04-22 12:08:19.934197 - Routing - green sent
    2 2014-04-22 12:08:19.934197 - Routing - green sent
    3 2014-04-22 12:08:19.934197 - Routing - green sent
    4 2014-04-22 12:08:19.934197 - Routing - green sent




.. code-block:: bash

    rangertaha@Coder:~/Projects/messaging-patterns/pubsub$ sudo rabbitmqctl list_bindings
    Listing bindings ...
        exchange	amq.gen-BXvvwbg12wVC3XJsPQPz9A	queue	amq.gen-BXvvwbg12wVC3XJsPQPz9A	[]
        exchange	basic	queue	basic	[]
        exchange	queue	queue	queue	[]
    exchange-001	exchange	amq.gen-BXvvwbg12wVC3XJsPQPz9A	queue	amq.gen-BXvvwbg12wVC3XJsPQPz9A	[]
    ...done.








Exchange
________

The exchange receives messages from the producer and sends them to queues.
 The exchange makes the discision of how to handle the message. It's
options are to append to a queue, append to many queues,
or discarded the message. The desision is based on the exchange types.


With respect to learning and clearifying things. I am representing the
exchange as a class.

.. code-block:: python

    #!/usr/bin/env python
    import pika
    from queue import Queue

    class Exchange(Queue):
        def __init__(self, exchange='exchange_001', type='direct'):
            Queue.__init__(self)
            self.channel.exchange_declare(exchange=exchange, type=type)
            self.exchange = exchange
            self.type = type










Consumers
________

.. code-block:: python

    #!/usr/bin/env python
    import sys
    import time
    from exchange import Exchange


    class Consumer(Exchange):
        def __init__(self):
            Exchange.__init__(self, exchange='exchange_001', type='direct')
            self.routing = sys.argv[1]
            self.bind()

        def bind(self):
            result = self.channel.queue_declare(exclusive=True)
            self.channel.queue_bind(exchange=self.exchange, queue=result.method
            .queue, routing_key=self.routing)
            self.queue = result.method.queue


        def callback(self, ch, method, properties, body):
            print '{0} received '.format(body)
            #time.sleep(5)

    if __name__ == '__main__':
        p = Consumer()
        p.receive()





.. code-block:: bash

    rangertaha@Coder:~/messaging-patterns/pubsub$ tty
    /dev/pts/3
    
    rangertaha@Coder:~/messaging-patterns/routing$ python consumer.py blue
    0 2014-04-22 12:08:08.657679 - Routing - blue received
    1 2014-04-22 12:08:08.657679 - Routing - blue received
    2 2014-04-22 12:08:08.657679 - Routing - blue received
    3 2014-04-22 12:08:08.657679 - Routing - blue received
    4 2014-04-22 12:08:08.657679 - Routing - blue received





.. code-block:: bash

    rangertaha@Coder:~/messaging-patterns/pubsub$ tty
    /dev/pts/4

    rangertaha@Coder:~/messaging-patterns/routing$ python consumer.py red
    0 2014-04-22 12:08:12.715046 - Routing - red received
    1 2014-04-22 12:08:12.715046 - Routing - red received
    2 2014-04-22 12:08:12.715046 - Routing - red received
    3 2014-04-22 12:08:12.715046 - Routing - red received
    4 2014-04-22 12:08:12.715046 - Routing - red received




.. code-block:: bash

    rangertaha@Coder:~/messaging-patterns/pubsub$ tty
    /dev/pts/5
    
    rangertaha@Coder:~/messaging-patterns/routing$ python consumer.py green
    0 2014-04-22 12:08:19.934197 - Routing - green received
    1 2014-04-22 12:08:19.934197 - Routing - green received
    2 2014-04-22 12:08:19.934197 - Routing - green received
    3 2014-04-22 12:08:19.934197 - Routing - green received
    4 2014-04-22 12:08:19.934197 - Routing - green received









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


