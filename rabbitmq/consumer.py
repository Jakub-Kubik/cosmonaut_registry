import json
import os

import pika
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models.cosmonaut import Cosmonaut, CosmonautCreate

# Load the .env file
load_dotenv(".env")

# Get RabbitMQ and other settings from environment variables
rabbitmq_host = os.getenv("RABBITMQ_HOST")
rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER")
rabbitmq_password = os.getenv("RABBITMQ_DEFAULT_PASS")
rabbitmq_queue_name = os.getenv("RABBITMQ_QUEUE_NAME")  # Default to "cosmonauts" if not set

# Setup RabbitMQ Connection
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
parameters = pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
session = Session(engine)


def callback(ch, method, properties, body):
    data = json.loads(body)

    # Convert the CosmonautCreate data into a Cosmonaut ORM object and validate it
    new_cosmonaut_data = CosmonautCreate(**data)
    new_cosmonaut = Cosmonaut(**new_cosmonaut_data.dict())

    # Store the new cosmonaut in the database
    session.add(new_cosmonaut)
    session.commit()


# Main RabbitMQ consumer setup
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue=rabbitmq_queue_name)  # Using the queue name from .env
channel.basic_consume(
    queue=rabbitmq_queue_name, on_message_callback=callback, auto_ack=True
)  # Using the queue name from .env

print(f" [*] Waiting for messages in queue {rabbitmq_queue_name}. To exit press CTRL+C")
channel.start_consuming()
