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