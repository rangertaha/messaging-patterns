A Basic Example
=================

This is the simplest pattern for sending messages I am using RabbitMQ as
the broker. This example has three parts. The **Producer**, **Queue**,
and the **Consumer**. The producer sends/produces messages which are sent to
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
______


The Queue is the RabbitMQ Server which uses AMQP to communicate.  This
receives messages, stores them and lets the consumer pick them up when ready.
Imagine your friend who you are texting has his phone turned off. The
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
            self.channel.basic_publish(exchange='', routing_key=self.queue,
                                       body=msg)

        def receive(self):
            self.channel.basic_consume(self.callback, queue=self.queue,
                                       no_ack=True)
            self.channel.start_consuming()







