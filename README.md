# Repository for Smart Contracts V2

> This project was built as part of a bachelor thesis about smart contract gas optimization. It is a full stack application that can be used to store and query information about smart contract source code.

## Version 2

Version 2 includes a complete redesign of frontend and backend. The API is now GET-only API with enhanced filter options and the client is updated accordingly. The application can be reached under https://scr.ide.tuhh.de/. This second version is fully functional and includes a larger set of query options that can be used to filter the data from the MongoDB collection. It also includes an enhanced client view that is build with vuejs and that consumes the API. The client view can statically be served.

## The Application

The **frontend** consists of a VueJS app that uses axios to call the API and BootstrapVue for styling. The code for the frontend can be found in `~/repo-smart-contracts/client` . The production server is served from the compiled and minified code in the `/dist` folder.

The **backend** consists of a python fastapi app that uses poetry as a dependency manager. The code for the backend can be found in `~/repo-smart-contracts/server`.

The **database** of this application is a MongoDB document store that is consumed by the fastapi service.

## Installation with Docker

- Establish environment: `cp server/example.env server/.env`
- Build project: `docker-compose build`
- Run project: `docker-compose up`

## Features

- Orchestration done with docker compose
- Frontend container with vueJS, bootstrap and axios
- Backend container with fastAPI, pydantic and poetry
- Database container with mongoDB
- Asynchronous OAS API with automatic documentation

---

## Hints for Developing

**Build:**
`docker-compose build`

**Run or Build single Container:**
`docker-compose up <mongo/api/client>`

**Run in Background:** Attach flag `-d`

---

**Using the OpenAPI from fastAPI**

Find the documentation: http://localhost:8081/redoc or http://localhost:8081/docs

Find the openapi schema: http://localhost:8081/openapi.json

---

**Interact with Mongo Shell:**

1. `docker-compose exec mongo bash`
2. `mongosh`
3. `use main_db`
4. `show contracts`
5. `db.contracts.<action>()`
