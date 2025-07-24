import pytest
import json
from rest_framework.test import APIClient
from app.users.models import User


@pytest.mark.django_db
class TestUserAPI:
    @pytest.fixture
    def client(self):
        return APIClient()

    def test_create_user_success(self, client):
        url = '/api/auth/users/'
        data = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "Password2000_",
            "re_password": "Password2000_"
        }
        response = client.post(url,
                               data=json.dumps(data),
                               content_type='application/json')
        assert response.status_code == 201

    def test_create_user_duplicate_email(self, client):
        User.objects.create_user(username='user1',
                                 email='dup@example.com',
                                 password='pass1234')

        url = '/api/auth/users/'
        data = {
            "username": "user2",
            "email": "dup@example.com",
            "password": "pass5678"
        }
        response = client.post(url,
                               data=json.dumps(data),
                               content_type='application/json')
        assert response.status_code == 400
        assert "email" in response.data

    def test_login_obtain_jwt_token(self, client):
        url = '/api/auth/jwt/create/'
        data = {
            "username": "userlogin",
            "password": "pass1234"
        }
        response = client.post(url,
                               data=json.dumps(data),
                               content_type='application/json')
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data
