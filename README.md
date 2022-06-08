# Repository for Smart Contracts

> Docker Compose with 3 Container: Frontend Vue, Backend FastAPI, Database MongoDB

### Fork from this resource

**Original Vue Template:**
https://vuejs-templates.github.io/webpack/

**Video:**
https://www.youtube.com/watch?v=4qYRs0Yzh9I

**Git:**
https://github.com/webdevjourneyWDJ/Docker_Projects/blob/master/server/src/app.js

### Hints for Developing

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

- `docker.compose exec mongo bash`
- `mongosh -u mongo_user -p mongo_password`
- `use main_db`
- `show collections`
- `db.contracts.drop()`
