# Open Weather API Service

Service that collects data from an Open Weather API for a user, stores the data in a MongoDB
database and provide the percentage of progress of a current post `weather` request. Uses FastAPI, Beanie (ODM for MongoDB) and Docker.

## Description

Endpoint for create users:

* /users/register -> POST request to register a user in the database.

Endpoints for collect weather data:

* /weather -> POST request to send external request to open weather api and store the data in database.
* /weather/{user_id} -> GET request to retrieve the percentage of a current post request a user has sent.

## Requirements

This project requires:

- Python version 3.11+

- Docker version 24

- A MongoDB GUI tool like Robo3T or MongoDB Altas

- Git version 2+

## Setup

### 1. Clone the repository

Clone this repository and change to the directory.

```bash
git clone https://github.com/Trjegul84/open_weather_service.git
```
### 2. Environment variables

Change the name of the file `.env.template` to `.env` and paste there the content of the following
s3 bucket `https://weatherapipersonalbucket.s3.amazonaws.com/credentials.txt`

### 3. Check available ports

If you already have other local applications or containers running check if the ports `8000` and `27017` are available and stop them temporary if needed or change the `docker-compose.yml` port mappings.

### 4. Run docker commands

In your prefered terminal run the following commands:

```bash

docker compose build

docker compose up -d

```

Check if the containers were created and are running with `docker ps`

If containers are running check the container name and use it to execute the following command
to check the logs of the container.

```bash
docker logs -f open_weather_api-fastapi
```

## Usage

Use your web browser or call the endpoints with another tool like insomnia, postman or with the curl command.

Open your browser and access the following url `http://localhost:8000/` it will redirect you to the `/docs` page with testing tools provided by FastAPI. Locate the endpoint you want to try and press the button `Try it out`. Enter the parameters required and press the `Execute` button.
The results will be shown in the `Responses` section.

Steps:

1. First you need to register a user:

Use the `/users/register` post endpoint in section Users. The username is optional. Once you execute the request a new `user_id` will be given. Save it to use other endpoints.


2. Execute a weather POST request:

With the previous user_id call tall the `/weather` **POST** endpoint in the WeatherData section. It is mandatory to input the value of the user_id. The application will initiate the process of sending requests to the Open Weather API and it will collect all the information about the weather for the list of cities configured in `app/settings.py`.
This endpoint returns only a message telling that your request is in progress. The weather data will be stored in the MongoDB database.


3. Get the percentage of the post request:

With the same `user_id` of the current POST request (in progress) you can check the percentage of registers already stored by using the **GET** endpoint `/weather/{user_id}` in the WeatherData section.
Once performed the request the result will appear in the responses section.

If a registered user has not made any POST request to collect data or the user_id does not exist a message will indicate the reason.

4. Check the documents in database:

To check the data stored in previous requests, access your mongodb GUI client and setup the host as `localhost` and the port `27017` also with no authentication.

#### Note:

>The script `request_sender.py` can be used to execute several GET `/weather/{user_id}` requests on your host (outside docker container) and check the percentage progress. An active virtual environment is needed.

## Tests

### **Pytest**

To execute tests `pytest` tool is used.

1. Use the name of the fastapi docker container (could it be similar to `open_weather_api-fastapi`) and enter:

```bash
docker exec -it open_weather_api-fastapi bash
```

2. Inside the container execute the command:

```bash
pytest -vvv
```

### **Coverage**
Inside the container execute the following commands to check the coverage percentage:

1. To test and get coverage information:
```bash
coverage run -m pytest -v
```
2. To check coverage information in user-friendly format:
```bash
coverage html
```
3. A new folder `htmlcov` will be generated. Locate the folder, find the file `htmlcov/index.html` and open it in a browser.

## About tools and frameworks:

**FastAPI**: it was designed for handling asynchronous requests and is one of the fastest Python web frameworks available due to its asynchronous nature and the efficient handling of requests. This makes it ideal for high-performance applications where response time and the ability to handle a large number of concurrent users are critical.
It makes possible to write concurrent code using the async/await syntax allowing to handle multiple requests concurrently without blocking the main thread, which is important for I/O-bound operations.

**Beanie**: is an Object Document Mapper (ODM) for MongoDB in Python, built on top of the popular asynchronous framework, Motor.  Is built for handling asynchronous operations and fits good for applications built using FastAPI, making possible to manage high number of concurrent database operations in an efficent way. Beanie also is integrated with Pydantic, getting the benefits of data type validation, data serialization/deserialization, type safety and model relationships.
Beanie simplifies CRUD database operations by providing direct methods that allows to handle MongoDB documents in a easier way.

**MongoDB**: is NoSQL document oriented database strongly compatible with async frameworks like FastAPI or Node.js. Its support for async operations improves systems which are designed to respond to events and changes in state therefore is good for real-time processing and responsiveness.
MongoDB’s document model is intuitive, easy and flexibe and is combined with powerful features like good query api and aggregations that allows developers to build responsive and complex applications that can handle large volumes of datasets.


## References

[FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/)

[Beanie](https://beanie-odm.dev/)

[Beanie example](https://dev.to/romanright/announcing-beanie-odm-18-relations-cache-actions-and-more-24ef)

[Beanie and FastAPI](https://jairoandres.com/fastapi-and-beanie/)

[MongoDB](https://www.mongodb.com/docs/mongodb-shell/crud/)

[Pydantic](https://docs.pydantic.dev/latest/)
