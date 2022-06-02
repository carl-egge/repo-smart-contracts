# Docker_Projects

Original Vue Template:
https://vuejs-templates.github.io/webpack/
Video:
https://www.youtube.com/watch?v=4qYRs0Yzh9I
Git:
https://github.com/webdevjourneyWDJ/Docker_Projects/blob/master/server/src/app.js

Build:
docker-compose build

Run Containter
docker-compose up mongo/api/client

- -d in background

Hot Reload Vue:

1. docker-compose up -d mongo
2. docker-compose up -d api
3. cd client
4. npm run dev

Enter Mongo Shell

- docker.compose exec mongo bash
- > mongosh -u mongo_user -p mongo_password
- > > use main_db
- > > show collections
- > > db.contracts.drop()
