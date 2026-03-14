# kafka-with-python

Python Producer Application

Setup: Installs the confluent-kafka Python library.
Logic: Simulates a customer placing an order by generating a JSON event (order ID, user, item, quantity).
Sending: Converts the JSON to bytes and produces it to a Kafka topic called new orders.
Reliability: Implements a delivery_report callback to track success/failure and uses producer.flush() to ensure all messages are sent before the program exits. 

** file : producer.py
import json
import uuid

from confluent_kafka import Producer

producer_config = { 'bootstrap.servers': 'localhost:9092'}

producer = Producer( producer_config)

#funcation

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result."""
    if err:
        print('Message delivery failed. Reason: {}'.format(err))
    else:
        print(f" Delivered {msg.value().decode('utf-8')}")
        print(f" Message delivered to Topic:  {msg.topic()}, Partition:  {msg.partition()} , Offset:  {msg.offset()} ")


order = {

    "order_id" : str(uuid.uuid4()),
    "user" : "ali",
    "item" : "burger",
    "quantity" : 1
}

order_value = json.dumps(order).encode("utf-8")

producer.produce(
    topic="orders",
    value=order_value,
    callback=delivery_report,
)
producer.flush()

--------------------------------------------------------------------------------------------
Python Consumer Application

Logic: Connects to the Kafka broker and subscribes to the new orders topic.
Processing: Uses a continuous while loop to poll for new messages.
Decoding: Receives bytes, converts them back to a Python dictionary, and prints the order details.
Graceful Shutdown: Implements a try-except block to catch KeyboardInterrupt and cleanly closes the consumer connection.

file: consumer.py

import json

from confluent_kafka import Consumer

consumer_config = { 'bootstrap.servers': 'localhost:9092',
                    'group.id': 'order_comsumer_id',
                    'auto.offset.reset': 'earliest', }

consumer = Consumer(consumer_config)

consumer.subscribe([
    "orders"
])

print("Consumer is running and connected and subscribed to Kafka topic :Orders:.")

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue

        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        value_ = msg.value().decode('utf-8')
        order = json.loads(value_)
        print(f"Received order of : {order['item']} with quantity {order['quantity']} from {order['user']}")
except KeyboardInterrupt:
    print("Shutting down consumer   ...")
    consumer.close()

finally:

    consumer.close()