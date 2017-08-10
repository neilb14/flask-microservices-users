## Build and run commands in container ##
```docker-compose up -d --build
docker-compose run users-service python manage.py recreate_db
docker exec -ti (docker ps -aqf "name=users-db") psql -U postgres
```


## Run Tests ##
```docker-compose run users-service python manage.py test
```