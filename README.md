# Spectate

- [Spectate](#spectate)
  - [Purpose](#purpose)
  - [User Stories](#user-stories)
  - [Database](#database)
    - [Configuration](#configuration)
    - [Structure](#structure)
    - [Notes](#notes)
  - [Deployment](#deployment)
    - [Environments](#environments)
  - [Code Standards](#code-standards)
    - [Notes](#notes-1)
  - [Documentation](#documentation)
  - [Testing](#testing)
  - [Local Development](#local-development)

## Purpose
The purpose of this service is to allow clients to retrieve sporting event data, create new events and update odds of existing events.

## User Stories

- As a developer I want to retrieve individual events by ID
- As a developer I want to retrieve a full list of events
- As a developer I want to filter for items by event name or sport name
- As a developer I want to sort results returned from the API
- As a developer I want to create new sporting events
- As a developer I want to provide the ID rather than use a default when creating an event
- As a developer I want to update the odds
- As a developer I want to use the POST method to create events and update odds
- As a developer I want to receive appropriate status codes and messages
- As a developer I want to receive accurate error messages
- As a developer I want to learn how to use these endpoints from the documentation

## Database

### Configuration
Local development is done with SQLite3, and in MySQL in production.

### Structure
The data structure can be found [here](docs/erd/erd.pdf)

### Notes
In order to keep ID constitant if the IDs of other systems that this service will integrate with, each table has `BigIntegerField` for the primary keys, rather than the default Django auto-increment field. This is to ensure that this service doesn't end up with different IDs for events than other services, which would make it difficult to look up the same 
events across different services.

This did, however, cause an issue with Django Rest Framework as it would throw a validation error when deserializing an event that already contained an ID that already existed in the database, even when this was expected for the `UpdateOdds` behaviour.

[Primary Key serialization issue resolution](https://stackoverflow.com/a/63782495)


## Deployment

Spectate is hosted on EC2, with a MySQL database running on RDS using Apache. The base URL is [here](http://ec2-3-250-80-154.eu-west-1.compute.amazonaws.com/api/match/).
### Environments
Environment management is handled by `django-environ` which loads in the environment variables from the `.env` file in the `spectate` app. This repository contains a `.env.example` as an example of what type of information is required. The main settings used are as follows:
- `DEBUG` (default: `False`)
  - The `DEBUG` value will default to `False`, make sure to set `DEBUG=on` when using development
- `SECRET_KEY` (default: `""`)
  - The `SECRET_KEY` is required by Django. Make sure to provide a `SECRET_KEY`
- `ALLOWED_HOST` (default: `127.0.0.1`)
  - This service is going to be on one server now, so a single item will be provided to Django's `ALLOWED_HOSTS` setting. If not provided, this will default to `127.0.0.1`. Be sure to update it to reflect the hostname of the system being used
- `CURRENT_DOMAIN` (default: `http://127.0.0.1:8000`)
  - Used to provided the full URL to the event. Defaults to `http://127.0.0.1:8000`
- `DATABASE_URI` (default: `""`)
  - The URI of the database to be used. If this is not provided, Django's default SQLite configuration will be used


## Code Standards
Code is formatted used Black with its default configuration. As a result, code will likely not pass normal PEP8 validation, specifically regarding line lengths.

### Notes
The field `start_time`, is written in standard PEP8 snake case formatting, however, the specification called for camel case (`startTime`). I have used [djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case) to render the field in the camel casing, which is the standard in languages like JS. This causes a slight inconsistency when using the `ordering` param to sort results. In order to sort results, the URL must be called with `ordering=start_time`, rather than `ordering=startTime`. I searched for a solution for this, however I was unable to find a straightforward answer.

## Documentation
The API is documented using the default configuration for [django-yasg](https://github.com/axnsan12/drf-yasg) using both Swagger and ReDoc. As the service is developed using Django Rest Framework, the API is [browsable](http://ec2-3-250-80-154.eu-west-1.compute.amazonaws.com/api/match/) by default, so most actions can be tested from here, however, [Swagger](http://ec2-3-250-80-154.eu-west-1.compute.amazonaws.com/swagger/) and [ReDoc](http://ec2-3-250-80-154.eu-west-1.compute.amazonaws.com/redoc/) documentation is also available.

## Testing
Automated testing was performed for both happy and unhappy paths to ensure that both, the correct information is returned, and also that error handling is effective and thorough. Testing was also performed through the browsable API and [Postman](docs/postman/Spectate.postman_collection.json).

## Local Development
In order to get this running locally, ensure that you have **SQLite**, **Python 3** and **virtualenv** installed and run the following commands:

```bash
git clone https://github.com/aaronsnig501/spectate.git
cd spectate
virtualenv env
. env/bin/activate
```

After this, you'll need to update add environment variables to the `.env` file, and from there run
```bash
python manage.py migrate
python manage.py createsuperuser # For any testing purposes
python manage.py runserver
```

In order to post any events you'll need to create a new `Sport` in the admin, and once that's ready you'll be able create new events.

Lastly, tests can be run using `python manage.py test`. Test fixtures are provided in `events/fixtures`