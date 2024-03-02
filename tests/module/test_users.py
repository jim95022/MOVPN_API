from pathlib import Path

import pytest

from app.users import UsersProcessor
from settings import CONFIG_FILE, CONFIG_FOLDER

username = "test_user"
default_users = ["phone", "laptop", "desktop"]


class TestUsers:

    @pytest.fixture
    def users(self, tmp_path):
        base_dir = Path(__file__).parent.parent

        config_template = base_dir / CONFIG_FILE
        path_to_config_folder = base_dir / CONFIG_FOLDER
        config_template_content = config_template.read_text()

        temp_config = tmp_path / config_template.name
        temp_config.write_text(config_template_content)

        return UsersProcessor(config_file=temp_config, config_folder=path_to_config_folder)

    def test_get_users(self, users):
        assert users.get() == default_users

    def test_add_user(self, users):
        users.add(username)
        assert users.get() == default_users + [username]

    def test_add_existing_user(self, users):
        existing_username = default_users[0]
        with pytest.raises(ValueError, match=rf".* {existing_username} .*"):
            users.add(existing_username)

    def test_remove_user(self, users):
        users.remove(default_users[0])
        assert users.get() == default_users[1:]

    def test_remove_not_existing_user(self, users):
        with pytest.raises(ValueError, match=rf".* {username} .*"):
            users.remove(username)

    def test_config_formatting(self, users):
        original_content = users.config_file.read_text()

        users.add(username)
        users.remove(username)

        modified_content = users.config_file.read_text()
        assert original_content == modified_content

    def test_get_qr_code(self, users):
        existing_username = default_users[0]
        qr_code_path = users.get_cred_path(f"{existing_username}.png")
        user_qr_code_path = users.config_folder / f"{existing_username}.png"
        assert qr_code_path == user_qr_code_path

    def test_get_not_existing_qr_code(self, users):
        with pytest.raises(FileNotFoundError):
            users.get_cred_path(f"{username}.png")
