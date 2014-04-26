Worker Queue
=================

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
________

A consumer is the application that receives the messages.


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
a different message from the set of messages the producer sends.

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


