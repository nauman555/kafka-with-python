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
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
        print(f" Delivered {msg.value().decode('utf-8')}")

order = {

    "order_id" : str(uuid.uuid4()),
    "user" : "ali",
    "item" : "burger",
    "quantity" : 10
}

order_value = json.dumps(order).encode("utf-8")

producer.produce(
    topic="orders",
    value=order_value,
    callback=delivery_report,
)
producer.flush()

