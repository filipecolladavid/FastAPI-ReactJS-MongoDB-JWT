# Template: FastAPI - ReactJS - MongoDB with JWT Authentication  

Template for starting a project with FARM stack. Dockerized, ready for deployment

## Development

1. Go to the directory where the frontend folder is located and run

```bash
  npm install
```
2. Go back to the root of the project and start the container

```bash
  docker-compose up
```

Both the frontend and the backend have auto-reload enabled, open the project on your IDE of choice and start development.

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

MongoDB

`MONGO_INITDB_ROOT_USERNAME`

`MONGO_INITDB_ROOT_PASSWORD`

`MONGO_INITDB_DATABASE`

`DATABASE_URL`


JWT

`ACCESS_TOKEN_EXPIRES_IN`

`REFRESH_TOKEN_EXPIRES_IN`

`JWT_ALGORITHM`

`JWT_PRIVATE_KEY` 

`JWT_PUBLIC_KEY`

CORS bypass for origin

`CLIENT_ORIGIN`

(See envExample)
