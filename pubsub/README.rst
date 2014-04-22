

Publish / Subscribe
=================


A publish/subscribe pattern allow a message can be past to multiple
consumers unlike the worker pattern. The producer sends
messages directly to the exchange where it follows its rules for
distributing the messages.




.. image:: ../images/pubsub.png





Producer
________

The producer sends messages to the exchange. Same as in the basic example


.. code-block:: python

    #!/usr/bin/env python
    from datetime import datetime
    from exchange import Exchange

    class Producer(Exchange):
        def __init__(self):
            Exchange.__init__(self, exchange='exchange-001', type='fanout')

        def send(self, msg):
            self.channel.basic_publish(exchange=self.exchange, routing_key='', body=msg)

    if __name__ == '__main__':
        NOW = datetime.now()
        p = Producer()
        for i in range(5):
            p.send('{0} {1} - Pub/Sub - Hello World'.format(i, NOW))
            print '{0} {1} - Pub/Sub - Hello World sent'.format(i, NOW)
        p.close()



.. code-block:: bash

    rangertaha@Coder:~/messaging-patterns/pubsub$ python producer.py
    0 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World sent
    1 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World sent
    2 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World sent
    3 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World sent
    4 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World sent


Use the **rabbitmqctl** command line admin tool to list the queues.

.. code-block:: bash

    rangertaha@Coder:~/messaging-patterns/pubsub$ sudo rabbitmqctl list_queues
    Listing queues ...
    basic	15
    ...done.









Exchange
________

The producer never sends messages directly to a queue but rather to the
exchange. The exchange receives messages from producers sends them to queues.
The exchange makes the discision of how to handle the message. It's
options are to append to a queue, append to many queues,
or discarded the message. The desision is based on the exchange types. The
following command show the types:

The rules, known as the exchange types are:
**direct**, **topic**, **headers** and **fanout**.


.. code-block:: bash

    rangertaha@Coder:~/messaging-patterns/pubsub$ sudo rabbitmqctl list_exchanges
    Listing exchanges ...
        direct
    amq.direct	direct
    amq.fanout	fanout
    amq.headers	headers
    amq.match	headers
    amq.rabbitmq.log	topic
    amq.rabbitmq.trace	topic
    amq.topic	topic
    ...done.
    



With respect to learning and clarifying things. I am representing the
exchange as a class.

.. code-block:: python

    #!/usr/bin/env python
    import pika
    from queue import Queue

    class Exchange(Queue):
        def __init__(self, exchange='exchange-001', type='fanout'):
            Queue.__init__(self)
            self.channel.exchange_declare(exchange=exchange, type=type)
            self.exchange = exchange
            self.type = type




Consumers
________



.. code-block:: python

    #!/usr/bin/env python
    import time
    from exchange import Exchange


    class Consumer(Exchange):
        def __init__(self):
            Exchange.__init__(self, exchange='exchange-001', type='fanout')
            self.bind()

        def bind(self):
            result = self.channel.queue_declare(exclusive=True)
            self.channel.queue_bind(exchange=self.exchange, queue=result.method.queue)
            self.queue = result.method.queue

        def callback(self, ch, method, properties, body):
            print '{0} received '.format(body)
            #time.sleep(5)

    if __name__ == '__main__':
        p = Consumer()
        p.receive(p.callback)






Here I am running 3 separate **consumer.py** on different terminals. Notice
the numbers at the start of the lines are all unique. Each consumer receives
a different message from the set of messages the producer sends.

.. code-block:: bash

    rangertaha@Coder:~/messaging-patterns/pubsub$ tty
    /dev/pts/7
    
    rangertaha@Coder:~/messaging-patterns/pubsub$ python consumer.py
    0 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World received
    1 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World received
    2 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World received
    3 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World received
    4 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World received




.. code-block:: bash

    rangertaha@Coder:~/messaging-patterns/pubsub$ tty
    /dev/pts/4

    rangertaha@Coder:~/messaging-patterns/pubsub$ python consumer.py
    0 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World received
    1 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World received
    2 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World received
    3 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World received
    4 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World received




.. code-block:: bash

    rangertaha@Coder:~/messaging-patterns/pubsub$ tty
    /dev/pts/9
    
    rangertaha@Coder:~/messaging-patterns/pubsub$ python consumer.py
    0 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World received
    1 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World received
    2 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World received
    3 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World received
    4 2014-04-22 09:39:16.483488 - Pub/Sub - Hello World received










Queue
______

The Queue is the RabbitMQ Server which uses AMQP to communicate.  This
receives messages, stores them and lets the consumer pick them up when ready.


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


