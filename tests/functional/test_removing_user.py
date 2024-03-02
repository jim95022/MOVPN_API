from pathlib import Path
from unittest.mock import patch

import pytest

from app.main import app
from app.users import UsersProcessor
from settings import CONFIG_FILE
from fastapi.testclient import TestClient


client = TestClient(app)
username = "test_user"
default_users = ["phone", "laptop", "desktop"]


class TestRemovingUser:

    @pytest.fixture
    def temp_config(self, tmp_path):
        base_dir = Path(__file__).parent.parent

        config_template = base_dir / CONFIG_FILE
        config_template_content = config_template.read_text()

        temp_config = tmp_path / config_template.name
        temp_config.write_text(config_template_content)

        return temp_config

    @pytest.fixture
    def users(self, temp_config):
        return UsersProcessor(config_file=temp_config, config_folder="")

    def test_removing_existing_user(self, users):

        with patch("app.main.users", users):
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

    def test_removing_not_existing_user(self, users):
        with patch("app.main.users", users):
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
