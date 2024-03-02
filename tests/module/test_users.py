import pytest

from tests.fixtures import fake_users_processor
from tests.defaults import default_users, username


class TestUsers:

    def test_get_users(self, fake_users_processor):
        assert fake_users_processor.get() == default_users

    def test_add_user(self, fake_users_processor):
        fake_users_processor.add(username)
        assert fake_users_processor.get() == default_users + [username]

    def test_add_existing_user(self, fake_users_processor):
        existing_username = default_users[0]
        with pytest.raises(ValueError, match=rf".* {existing_username} .*"):
            fake_users_processor.add(existing_username)

    def test_remove_user(self, fake_users_processor):
        fake_users_processor.remove(default_users[0])
        assert fake_users_processor.get() == default_users[1:]

    def test_remove_not_existing_user(self, fake_users_processor):
        with pytest.raises(ValueError, match=rf".* {username} .*"):
            fake_users_processor.remove(username)

    def test_config_formatting(self, fake_users_processor):
        original_content = fake_users_processor.config_file.read_text()

        fake_users_processor.add(username)
        fake_users_processor.remove(username)

        modified_content = fake_users_processor.config_file.read_text()
        assert original_content == modified_content

    def test_get_qr_code(self, fake_users_processor):
        existing_username = default_users[0]
        qr_code_path = fake_users_processor.get_cred_path(f"{existing_username}.png")
        user_qr_code_path = fake_users_processor.config_folder / f"{existing_username}.png"
        assert qr_code_path == user_qr_code_path

    def test_get_not_existing_qr_code(self, fake_users_processor):
        with pytest.raises(FileNotFoundError):
            fake_users_processor.get_cred_path(f"{username}.png")
