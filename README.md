# Template: FastAPI - ReactJS - MongoDB with JWT Authentication  

Template for starting a project with FARM stack. Dockerized, ready for deployment


## Deployment

To deploy this project run

```bash
  docker-compose up
```


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
## Development

Both backend and frontend have auto-reload enabled, so just start the container and open the project in an IDE and start development
