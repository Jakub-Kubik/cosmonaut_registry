# Cosmonaut Registry

## Introduction

This project is an application for storing ald reading a database of cosmonauts.
It includes create (C) and read (R) from CRUD operations.
C is implemented via RabbitMQ by producent-consumer pattern with one queue.
R is implemented via RESTful API, which is built with FastAPI framework.

## Features

- RESTful API for reading built with FastAPI
- RabbitMQ for asynchronous data storing
- PostgreSQL database backend
- Everything is dockerized for easy deployment

## Installation and Setup

### Requirements

- Docker and Docker Compose

### Local Development

1. Clone the repository:

    ```
    git clone https://github.com/your_username/cosmonaut_registry.git
    ```

2. Navigate into the project directory:

    ```
    cd cosmonaut_registry
    ```

3. Update all env variables and credentials in `.env`:

4. Build and start all Docker containers:

    ```
    docker-compose up
    ```

Ideally you should at first run rabbitMQ for loading all the data into database and then run the FastAPI application.

5. The FastAPI application is running at [http://localhost:8000](http://localhost:8000).

### Running the RabbitMQ Producer and Consumer

After setting up your environment, you can run the RabbitMQ producer and consumer by:

    ```
    docker-compose up rabbitmq_producer rabbitmq_consumer
    ```

## Usage

You can perform CRUD operations through the API:

- **Read Cosmonaut**: `GET /cosmonaut/{cosmonaut_id}`

To see all available API routes, visit the auto-generated documentation at [http://localhost:8000/docs](http://localhost:8000/docs).
