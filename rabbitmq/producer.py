import json
import os
from random import choice, randint, uniform

import pika
from dotenv import load_dotenv
from faker import Faker

# Load the .env file
load_dotenv(".env")

fake = Faker()

# Get RabbitMQ and queue settings from environment variables
rabbitmq_host = os.getenv("RABBITMQ_HOST")
rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER")
rabbitmq_password = os.getenv("RABBITMQ_DEFAULT_PASS")
rabbitmq_queue_name = os.getenv("RABBITMQ_QUEUE_NAME")
num_messages = int(os.getenv("NUM_MESSAGES", 0))

# Setup RabbitMQ Connection
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
parameters = pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue=rabbitmq_queue_name)

for i in range(num_messages):  # Using the value from .env
    random_cosmonaut_data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "age": randint(20, 60),
        "gender": choice(["male", "female"]),
        "nationality": fake.country(),
        "specialization": choice(["Engineer", "Doctor", "Physicist", "Chemist"]),
        "time_in_space": round(uniform(0, 500), 2),
    }

    channel.basic_publish(exchange="", routing_key=rabbitmq_queue_name, body=json.dumps(random_cosmonaut_data))

connection.close()
