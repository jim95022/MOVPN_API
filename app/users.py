import re
from pathlib import Path
from typing import Any


class UsersProcessor:

    usernames_pattern = r"users:\s+((- .*?\s+)+)"

    def __init__(self, config_file: Path | str, config_folder: str):
        if isinstance(config_folder, str):
            config_file = Path(config_file)
        self.config_file = config_file
        self.config_folder = config_folder

    def _update_config_with_users(self, users):
        config_content = self.config_file.read_text()
        users_formatted = [f"  - {user}" for user in users]
        new_users_formatted = "users:\n" + "\n".join(users_formatted) + "\n\n"
        config_content_updated = re.sub(self.usernames_pattern, new_users_formatted, config_content)
        self.config_file.write_text(config_content_updated)

    def get(self) -> list:
        content = self.config_file.read_text()
        raw_match = re.search(self.usernames_pattern, content)

        usernames = []

        if raw_match:
            raw_usernames = raw_match[1]
            usernames = raw_usernames.replace(" ", "").replace("\n", "").split("-")
            usernames = [username for username in usernames if len(username) > 0]

        return usernames

    def add(self, username: str) -> None:
        users = self.get()

        if username in users:
            raise ValueError(f"The user {username} is already in the list")

        users.append(username)
        self._update_config_with_users(users)

    def retrieve_creds(self, username: str) -> Any:
        raise NotImplementedError

    def remove(self, username: str) -> None:
        users = self.get()

        if username not in users:
            raise ValueError(f"The user {username} is not in the list")

        users.remove(username)
        self._update_config_with_users(users)
