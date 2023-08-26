## Getting Started

The application has been containerized and is ready to run via `docker-compose`. It first needs to be initialized,
creating the admin user. This can be accomplished by running:

    $ docker-compose run init

Once the application is initialized, the whole stack can be brought up using:


    $ docker-compose up -d

The stack includes:
- An application server (Python/Flask), which will be exposed on port 5000 of the host machine.
- A database (MongoDB), which will be exposed on the default MongoDB port.
- A web application to interact directly with the database (Mongo Express), for testing & inspection purposes. This is 
exposed on port 8081, with a u/p of admin/pass.

## Tests

Both unit and integration tests were written for this assignment. They can be found in `tests/`

Unit tests can be run with:


    $ docker-compose run unittest

Integration tests can be run with:


    $ docker-compose run apitest

## API

The API was implemented using Python and Flask. It currently supports two sets of operations: ECG operations and Auth
operations. All endpoints are documented in docstrings in `app.py`.

The ECG endpoints were built according to the requirements provided. I chose to build a JWT-based auth system, though
as the application scales, I would recommend using an auth framework, or even a third party application like Auth0.

## Next Steps

There are a number of improvements I would make to this application:

- The built-in Flask web server is not suited for production use. Something like gunicorn or another WSGI server would
  be better suited to a production environment.
- Separate Dockerfiles could be created for test, which do not include all of the dependencies of the main image. This
  would speed up the time needed to build these images, for example if they were to be included in a CI/CD pipeline.
- Unit and integration testing coverage should be increased, and the integration tests could be cleaned up.
- Marshmallow could be used for (de)serialization and validation of API inputs and responses.
- Thorough API documentation could be created using Swagger.
- A review of the HTTP status codes could be performed -- I defaulted to 200/201/400 in most cases. This should be 
  reviewed and expanded.
- No attention was paid to logging.

## Scalability/performance

As the application scales, there are a few things worth thinking about.

- Auth can be moved into a separate microservice, or out to a 3rd party.
- MongoDB can be scaled for increased performance and replication.
- Multiple instances of the application can be run and put behind a load balancer

Further to this, if more compute-intensive processing tasks are required, it may be interesting to perform these 
asynchronously at load time. I would suggest using something like Celery for handling these tasks in the background,
creating accompanying collections of already-processed data in the database.