from unittest.mock import patch


from tests.fixtures import client, fake_users_processor
from tests.defaults import username


class TestRetrieveCreds:

    def test_retrieve_creds_of_existing_user(self, client, fake_users_processor):
        with patch("app.main.users", fake_users_processor):
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
            user_qr_code_path = fake_users_processor.config_folder / f"{existing_user}.png"
            user_conf_path = fake_users_processor.config_folder / f"{existing_user}.conf"

            assert qr_code.content == user_qr_code_path.read_bytes()
            assert conf.content == user_conf_path.read_bytes()

    def test_retrieve_creds_of_not_existing_user(self, client, fake_users_processor):
        with patch("app.main.users", fake_users_processor):
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
