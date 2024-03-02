from unittest.mock import patch

from tests.fixtures import client, default_users, fake_users_processor, username


class TestRemovingUser:

    def test_removing_existing_user(self, fake_users_processor):

        with patch("app.main.users", fake_users_processor):
            # Get all users
            response = client.get("/users")
            assert response.status_code == 200
            assert response.json() == {"users": default_users}

            # Remove existing user
            existing_user = default_users[0]
            response = client.delete(f"/users/{existing_user}")
            assert response.status_code == 202

            # Get all users
            response = client.get("/users")
            assert response.status_code == 200
            assert response.json() == {"users": default_users[1:]}

    def test_removing_not_existing_user(self, fake_users_processor):
        with patch("app.main.users", fake_users_processor):
            # Get all users
            response = client.get("/users")
            assert response.status_code == 200
            assert response.json() == {"users": default_users}

            # Remove not existing user
            response = client.delete(f"/users/{username}")
            assert response.status_code == 400

            # Get all users
            response = client.get("/users")
            assert response.status_code == 200
            assert response.json() == {"users": default_users}
