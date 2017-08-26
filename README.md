![Build Status](https://travis-ci.org/neilb14/flask-microservices-users.svg?branch=master)

##Env Cheatsheet##
Remember that Docker container's build context is the Github remote master branch. So you gotta push your changes and rebuild containers in order for them to work.

###Variables###
Set the following environment variables:
```export SECRET_KEY=xxx```
```export DATABASE_URL=xxx```
```export DATABASE_TEST_URL=xxx```

###Tests###
Run tests:
```python manage.py test```

###Database###
Create the database:
```python manage.py recreate_db```

###Migrations###
After changing a model:
```
python manage.py db migrate
python manage.py db upgrade
```
