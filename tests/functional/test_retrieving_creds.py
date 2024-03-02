from pathlib import Path
from unittest.mock import patch

import pytest

from app.main import app
from app.users import UsersProcessor
from settings import CONFIG_FILE, CONFIG_FOLDER
from fastapi.testclient import TestClient


client = TestClient(app)
username = "test_user"
default_users = ["phone", "laptop", "desktop"]


class TestRetrieveCreds:

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
        base_dir = Path(__file__).parent.parent
        config_folder = base_dir / CONFIG_FOLDER
        return UsersProcessor(config_file=temp_config, config_folder=config_folder)

    def test_retrieve_creds_of_existing_user(self, users):
        with patch("app.main.users", users):
            # get all users
            response = client.get("/users")
            assert response.status_code == 200

            # retrieve one existing user
            response_json = response.json()
            existing_user = response_json["users"][0]

            # retrieve qr code and cert of existing user
            qr_code = client.get(f"/users/{existing_user}/qr")
            conf = client.get(f"/users/{existing_user}/conf")

            # assert qr_code, cert with existing
            user_qr_code_path = users.config_folder / f"{existing_user}.png"
            user_conf_path = users.config_folder / f"{existing_user}.conf"

            assert qr_code.content == user_qr_code_path.read_bytes()
            assert conf.content == user_conf_path.read_bytes()

    def test_retrieve_creds_of_not_existing_user(self, users):
        with patch("app.main.users", users):
            # get all users
            response = client.get("/users")
            assert response.status_code == 200

            # verify user does not exit
            response_json = response.json()
            assert username not in response_json["users"]

            # retrieve qr code and cert of not existing user
            response = client.get(f"/users/{username}/qr")
            assert response.status_code == 400

            response = client.get(f"/users/{username}/conf")
            assert response.status_code == 400
