## Build and run commands in container ##
You can grab the IP address of the machine
```$ docker-machine ip dev```

And some various commands to create the environment and database:
```docker-compose up -d --build
docker-compose run users-service python manage.py recreate_db
docker exec -ti (docker ps -aqf "name=users-db") psql -U postgres
```


## Run Tests ##
```docker-compose run users-service python manage.py test
```