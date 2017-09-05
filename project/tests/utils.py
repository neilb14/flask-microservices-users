import datetime, json
from flask import request

from project import db
from project.api.models import User

def add_user(username, email, password='password123', created_at=datetime.datetime.utcnow()):
        user = User(username=username, email=email, password=password, created_at=created_at)
        db.session.add(user)
        db.session.commit()
        return user

def login_test_user(client):
        add_user('test_user','test@user.com')
        resp_login = client.post('/auth/login',
                data=json.dumps(dict(email='test@user.com',password='password123')),
                content_type='application/json'
        )
        return dict(Authorization='Bearer ' + json.loads(resp_login.data.decode())['auth_token'])
