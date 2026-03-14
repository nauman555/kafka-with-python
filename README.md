# kafka-with-python

Python Producer Application

Setup: Installs the confluent-kafka Python library.
Logic: Simulates a customer placing an order by generating a JSON event (order ID, user, item, quantity).
Sending: Converts the JSON to bytes and produces it to a Kafka topic called new orders.
Reliability: Implements a delivery_report callback to track success/failure and uses producer.flush() to ensure all messages are sent before the program exits. 

Python Consumer Application

Logic: Connects to the Kafka broker and subscribes to the new orders topic.
Processing: Uses a continuous while loop to poll for new messages.
Decoding: Receives bytes, converts them back to a Python dictionary, and prints the order details.
Graceful Shutdown: Implements a try-except block to catch KeyboardInterrupt and cleanly closes the consumer connection.