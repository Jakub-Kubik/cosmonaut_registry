import json
import os

import pika
from dotenv import load_dotenv

# Load the .env file
load_dotenv(".env")

# Get RabbitMQ settings from environment variables
rabbitmq_host = os.getenv("RABBITMQ_HOST")
rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER")
rabbitmq_password = os.getenv("RABBITMQ_DEFAULT_PASS")

# Setup RabbitMQ Connection
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
parameters = pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue="cosmonauts")

cosmonaut_data = {
    "first_name": "John",
    "last_name": "Doe",
    "age": 30,
    "gender": "male",
    "nationality": "American",
    "specialization": "Engineer",
    "time_in_space": 181.0,
}

channel.basic_publish(exchange="", routing_key="cosmonauts", body=json.dumps(cosmonaut_data))

print(f" [x] Sent {cosmonaut_data}")

connection.close()
