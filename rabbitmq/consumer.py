import json
import os
import threading
from threading import local

import pika
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.cosmonaut import Base, Cosmonaut, CosmonautCreate

# Load the .env file
load_dotenv(".env")

# Get RabbitMQ and other settings from environment variables
rabbitmq_host = os.getenv("RABBITMQ_HOST")
rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER")
rabbitmq_password = os.getenv("RABBITMQ_DEFAULT_PASS")
rabbitmq_queue_name = os.getenv("RABBITMQ_QUEUE_NAME")

# Setup RabbitMQ Connection
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
parameters = pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)

# Initialize a thread-local data storage
thread_local = local()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))

# Create all tables if they are already not created
Base.metadata.create_all(engine)


def callback(ch, method, properties, body):
    if not hasattr(thread_local, "bulk_data"):
        thread_local.bulk_data = []

    if not hasattr(thread_local, "session"):
        thread_local.session = Session()

    session = thread_local.session
    bulk_data = thread_local.bulk_data

    data = json.loads(body)
    new_cosmonaut_data = CosmonautCreate(**data)
    new_cosmonaut = Cosmonaut(**new_cosmonaut_data.dict())

    bulk_data.append(new_cosmonaut)

    ##########################################
    # benchmark 3
    ##########################################
    # Store the new cosmonaut in the database
    # session.add(new_cosmonaut)
    # session.commit()

    ##########################################
    # benchmark 4
    ##########################################
    if len(bulk_data) >= 100:
        session.bulk_save_objects(bulk_data)
        session.commit()
        bulk_data.clear()


def start_consumer():
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=rabbitmq_queue_name)
    channel.basic_consume(queue=rabbitmq_queue_name, on_message_callback=callback, auto_ack=True)

    print(f" [*] Waiting for messages in queue {rabbitmq_queue_name}. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    for i in range(5):
        threading.Thread(target=start_consumer).start()
