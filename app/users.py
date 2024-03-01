import re
from pathlib import Path
from typing import Any


class UsersProcessor:

    def __init__(self, config_file: Path, config_folder: str):
        self.config_file = config_file
        self.config_folder = config_folder

    def get(self) -> list:
        usernames_pattern = r"users:\s+((- .*?\s+)+)"
        content = self.config_file.read_text()
        raw_match = re.search(usernames_pattern, content)

        usernames = []

        if raw_match:
            raw_usernames = raw_match[1]
            usernames = raw_usernames.replace(" ", "").replace("\n", "").split("-")
            usernames = [username for username in usernames if len(username) > 0]

        return usernames

    def add(self, username: str) -> None:
        pass

    def retrieve_creds(self, username: str) -> Any:
        raise NotImplementedError

    def remove(self, username: str) -> None:
        raise NotImplementedError
