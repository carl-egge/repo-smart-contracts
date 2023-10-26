# Repository for Smart Contracts V3

> This project was built from the researchers at the Institut of Data Engineering at the TUHH. It is a full stack application that can be used to store and query information about smart contract source code. It serves the purpose of running gas optimization analysis on blockchain source code.

## Version 3

Version 3 of the Smart Contract Repository is now build to serve two different collection of data. First a collection _contracts_ with Solidity files is provided. Secondly the collection _flatcontracts_ holds Solidity Smart Contracts that were merged by a flatting tool and that should be compilable without any dependencies. The goal with this second smaller collection of flattened contracts is to make the analysis of the versioned source code easier. Most established analysis tools in the area of Smart Contracts require a flat source code similar to how etherscan.io requires a flat contract in order to verify it. Therefore the collection _flatcontracts_ is additionally provided. Both collections can be query and filtered using the python-based API. The updated code for the client vue application also features the two different collections. 

## The Application

The application can be reached under https://scr.ide.tuhh.de/.

Under the live application further information on the project and the dataset can be found. To check the documentation of the live application go to: https://scr.ide.tuhh.de/api/docs.

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
