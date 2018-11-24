# REST-based Codenar response 

## Overview

We are uphauling codenar by building RESTful APIs for 
1. All scans
2. Subdomain scans
3. SSL scans
4. IP scans
5. DNS scans

## Local Development Setup

Use Python 3.6, Docker, and Docker Compose.

Step 1. 
Make a Python 3.6.x virtualenv.

Step 2.
Copy env.template to .env and adjust values to match your local environment:

    cp env.template .env

Step 3.
Create a new .version file:

    touch .version

Then run

    docker-compose up

This will create the Docker image, install dependencies, start the services defined in `docker-compose.yaml`, and start the webserver.

## Running the tests

To run the tests, execute:

    docker-compose run --rm web pytest

## Deploying

TDB

## Production Environment Considerations

TDB

