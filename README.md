# Repository for Smart Contracts V2

> This project was built as part of a bachelor thesis about smart contract gas optimization. It is a full stack application that can be used to store and interact with smart contract source code.

## Version 2

Version 2 will include a complete redesign of frontend and backend. The API will be a GET-only API with enhanced filter options and the client will be updated accordingly.

## Installation

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

**Hot Reload for Vue without Docker:**

1. `docker-compose up -d mongo`
2. `docker-compose up -d api`
3. `cd client`
4. `npm run dev`

---

**Enter Mongo Shell:**

1. `docker-compose exec mongo bash`
2. `mongosh`
3. `use main_db`
4. `show collections`
5. `db.<collection_name>.<action>()`
