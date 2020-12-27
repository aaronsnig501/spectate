# Spectate

- [Spectate](#spectate)
  - [Purpose](#purpose)
  - [User Stories](#user-stories)
  - [Data Structure](#data-structure)

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

## Data Structure
The data structure can be found [here](docs/erd/erd.pdf)


Primary Key serialization issue resolution: https://stackoverflow.com/a/63782495