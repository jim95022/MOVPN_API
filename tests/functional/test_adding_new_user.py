from unittest.mock import patch

from tests.fixtures import client, default_users, username, fake_users_processor


class TestNewUser:

    def test_adding_not_existing_user(self, fake_users_processor):

        with patch("app.main.users", fake_users_processor):

            # Get all users
            response = client.get("/users")
            assert response.status_code == 200
            assert response.json() == {"users": default_users}

            # Add new user
            response = client.post(f"/users/{username}")
            assert response.status_code == 201

            # Get all users
            response = client.get("/users")
            assert response.status_code == 200
            assert response.json() == {"users": default_users + [username]}

    def test_adding_existing_user(self, fake_users_processor):
        with patch("app.main.users", fake_users_processor):
            # Get all users
            response = client.get("/users")
            assert response.status_code == 200
            assert response.json() == {"users": default_users}

            # Add an existing user
            existing_user = default_users[0]
            response = client.post(f"/users/{existing_user}")
            assert response.status_code == 400

            # Get all users
            response = client.get("/users")
            assert response.status_code == 200
            assert response.json() == {"users": default_users}
