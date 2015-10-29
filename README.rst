Example Messaging Patterns
==========================

These are simple example based tutorials for developing
basic messaging applications with `RabbitMQ <https://www.rabbitmq.com/download.html>`_.
RabbitMQ and the `Pika <https://github.com/pika/pika/>`_  Python library
must be installed to run the code examples


Installation
------------

    * Install `RabbitMQ <https://www.rabbitmq.com/download.html>`_
    * Install `Pika <https://github.com/pika/pika/>`_


Basic Patterns
--------------

This is the simplest pattern for sending messages. I am using RabbitMQ as
the broker. This example has three parts, the **Producer**, **Queue**,
and **Consumer**. The producer sends/produces messages which are sent to
the queue. The queue is the RabbitMQ server. The consumer
retrieves/consumes the messages from the queue.


.. image:: ../images/basic.png



Producer
________

A producer is the application that sends the messages. Imagine sending text
messages to your friend.

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

    rangertaha@Coder:~/messaging-patterns/basic$ python producer.py
    0 2014-04-22 00:19:59.497745 - Basic - Hello World sent
    1 2014-04-22 00:19:59.497745 - Basic - Hello World sent
    2 2014-04-22 00:19:59.497745 - Basic - Hello World sent
    3 2014-04-22 00:19:59.497745 - Basic - Hello World sent
    4 2014-04-22 00:19:59.497745 - Basic - Hello World sent


Use the **rabbitmqctl** command line admin tool to list the queues.

.. code-block:: bash

    rangertaha@Coder:~/messaging-patterns/basic$ sudo rabbitmqctl list_queues
    Listing queues ...
    basic	5
    ...done.





Consumer
________

A consumer is the application that receives the messages. Imagine your friend
who is receiving your text messages.


.. code-block:: python

    #!/usr/bin/env python
    from queue import Queue

    class Consumer(Queue):
        def __init__(self):
            Queue.__init__(self, queue='basic')

        def callback(self, ch, method, properties, body):
            print '{0} received '.format(body)

    if __name__ == '__main__':
        p = Consumer()
        p.receive()


The following is the execution and output of the consumer.py script.

.. code-block:: bash

    rangertaha@Coder:~/messaging-patterns/basic$ python consumer.py
    0 2014-04-22 00:19:59.497745 - Basic - Hello World received
    1 2014-04-22 00:19:59.497745 - Basic - Hello World received
    2 2014-04-22 00:19:59.497745 - Basic - Hello World received
    3 2014-04-22 00:19:59.497745 - Basic - Hello World received
    4 2014-04-22 00:19:59.497745 - Basic - Hello World received





Queue
_____


The Queue is the RabbitMQ Server which uses AMQP to communicate.  This
receives messages, stores them and lets the consumer pick them up when ready.
Imagine texting your friend, who has his phone turned off. The
messages you send are placed in the Queue until his phone is turned back
on and he receives the messages.


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
            self.channel.basic_publish(exchange='', routing_key=self.queue,
                                       body=msg)

        def receive(self):
            self.channel.basic_consume(self.callback, queue=self.queue,
                                       no_ack=True)
            self.channel.start_consuming()





Worker
------

This is an example of a work queue. This type of queue is used to
distribute messages to multiple workers. It is the second simplest pattern for sending messages, the fist being the
basic. This example also has three parts.  The **Producer**, **Queue**,
and the **Consumers**. The producer sends/produces messages which are sent to
the queue. The queue is the RabbitMQ server. The consumers
retrieve/consume the messages from the queue. We can have as many
consumers as we want. The messages are evenly distributed among them.


.. image:: ../images/worker.png










Producer
________

This producer is the same as the previous basic example. It is the application
that sends the messages.


.. code-block:: python

    #!/usr/bin/env python
    from datetime import datetime
    from queue import Queue

    class Producer(Queue):
        def __init__(self):
            Queue.__init__(self, queue='basic')

    if __name__ == '__main__':
        NOW = datetime.now()
        p = Producer()
        for i in range(15):
            p.send('{0} {1} - Basic - Hello World'.format(i, NOW))
            print '{0} {1} - Basic - Hello World sent'.format(i, NOW)
        p.close()


.. code-block:: bash

    rangertaha@Coder:~/messaging-patterns/workers$ python producer.py
    0 2014-04-22 00:10:16.946810 - Basic - Hello World sent
    1 2014-04-22 00:10:16.946810 - Basic - Hello World sent
    2 2014-04-22 00:10:16.946810 - Basic - Hello World sent
    3 2014-04-22 00:10:16.946810 - Basic - Hello World sent
    4 2014-04-22 00:10:16.946810 - Basic - Hello World sent
    5 2014-04-22 00:10:16.946810 - Basic - Hello World sent
    6 2014-04-22 00:10:16.946810 - Basic - Hello World sent
    7 2014-04-22 00:10:16.946810 - Basic - Hello World sent
    8 2014-04-22 00:10:16.946810 - Basic - Hello World sent
    9 2014-04-22 00:10:16.946810 - Basic - Hello World sent
    10 2014-04-22 00:10:16.946810 - Basic - Hello World sent
    11 2014-04-22 00:10:16.946810 - Basic - Hello World sent
    12 2014-04-22 00:10:16.946810 - Basic - Hello World sent
    13 2014-04-22 00:10:16.946810 - Basic - Hello World sent
    14 2014-04-22 00:10:16.946810 - Basic - Hello World sent
    rangertaha@Coder:~/messaging-patterns/workers$



Use the **rabbitmqctl** command line admin tool to list the queues.


.. code-block:: bash

    rangertaha@Coder:~/messaging-patterns/workers$ sudo rabbitmqctl list_queues
    Listing queues ...
    basic	15
    ...done.

















Consumers
_________

A consumer is the application that receives the messages. This consumer
receives a message and prints it to the terminal. It then waits 1 second
before doing it again.


.. code-block:: python

    #!/usr/bin/env python
    import time
    from queue import Queue

    class Consumer(Queue):
        def __init__(self):
            Queue.__init__(self, queue='basic')

        def callback(self, ch, method, properties, body):
            print 'Received: {0}'.format(body)
            time.sleep(1)

    if __name__ == '__main__':
        p = Consumer()
        p.receive(p.callback)


Here I am running 3 separate **consumer.py** on different terminals. Notice
the numbers at the start of the lines are all unique. Each consumer receives
a different message from the set of messages the producer sends. They each
process one message and wait one second then repeat the process.

.. code-block:: bash

    rangertaha@Coder:~/messaging-patterns/workers$ python consumer.py
    0 2014-04-22 00:10:16.946810 - Basic - Hello World received
    3 2014-04-22 00:10:16.946810 - Basic - Hello World received
    6 2014-04-22 00:10:16.946810 - Basic - Hello World received
    9 2014-04-22 00:10:16.946810 - Basic - Hello World received
    12 2014-04-22 00:10:16.946810 - Basic - Hello World received



.. code-block:: bash

    rangertaha@Coder:~/messaging-patterns/workers$ python consumer.py
    1 2014-04-22 00:10:16.946810 - Basic - Hello World received
    4 2014-04-22 00:10:16.946810 - Basic - Hello World received
    7 2014-04-22 00:10:16.946810 - Basic - Hello World received
    10 2014-04-22 00:10:16.946810 - Basic - Hello World received
    13 2014-04-22 00:10:16.946810 - Basic - Hello World received



.. code-block:: bash

    rangertaha@Coder:~/messaging-patterns/workers$ python consumer.py
    2 2014-04-22 00:10:16.946810 - Basic - Hello World received
    5 2014-04-22 00:10:16.946810 - Basic - Hello World received
    8 2014-04-22 00:10:16.946810 - Basic - Hello World received
    11 2014-04-22 00:10:16.946810 - Basic - Hello World received
    14 2014-04-22 00:10:16.946810 - Basic - Hello World received









Queue
______

The Queue is the RabbitMQ Server which uses AMQP to communicate.  This
receives messages, stores them, and lets the consumer pick them up when ready.
Imagine texting your friend, who has his phone turned off. The
messages you send are placed in the Queue until his phone is turned back
on and receives the messages.

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





Publish/Subscribe
-----------------

A publish/subscribe pattern allows a message to be passed to multiple
consumers, unlike the worker pattern. The producer sends
messages directly to the exchange, where it follows its rules for
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
exchange. The exchange receives messages from producers and sends them to queues.
The exchange makes the decision on how to handle the message. Its
options are to append to a queue, append to many queues,
or discard the message. The decision is based on the exchange types. The
following commands show the types:

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
_________



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
that the numbers at the start of the lines are all unique. Each consumer receives
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
_____

The Queue is the RabbitMQ Server, which uses AMQP to communicate.  This
receives messages, stores them, and lets the consumer pick them up when ready.


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




Routing
-------



This routing pattern uses the exchange type **direct** and a **routing_key**
. Consumers use this key to accessing the messages from the queue.


.. image:: ../images/routing.png


Producer
________

The producer sends messages to the exchange. In this example we are using an
exchange with the **direct** type. This producer also takes an argument wich
 is assigned as the **routing_key**.



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


Bellow you can see I ran the producer with the **blue**, **red**,
and then **green** as a single argument. This argument is assigned as the
**routing_key**. Consumers will need this key to retrieve the message.

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
The exchange makes the decision of how to handle the message. Its
options are to append to a queue, append to many queues,
or discard the message. The decision is based on the exchange types.

This is an example of the **direct** type. With respect to clarity. I am
representing the exchange as a class.

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
_________

A consumer is the application that receives the messages. This consumer
takes one argument which is assigned as the  **routing_key**. It then prints
all messages with that **routing_key** to the terminal.

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


    if __name__ == '__main__':
        p = Consumer()
        p.receive()


In these examples the consumer is given an argument which is the
**routing_key**. It then retrieves the messages that have that **routing_key**.


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
_____

The Queue is the RabbitMQ Server which uses AMQP to communicate.  This
receives messages, stores them, and lets the consumer pick them up when ready.

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






ToDo
----


Topic
_____

.. image:: ./images/topic.png



Remote Procedure Call (RPC)
_____

.. image:: ./images/rpc.png
