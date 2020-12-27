# Spectate

- [Spectate](#spectate)
  - [Purpose](#purpose)
  - [User Stories](#user-stories)
  - [Database](#database)
    - [Configuration](#configuration)
    - [Structure](#structure)
    - [Notes](#notes)

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

Primary Key serialization issue resolution: https://stackoverflow.com/a/63782495