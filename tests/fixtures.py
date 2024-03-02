from pathlib import Path

import pytest
from starlette.testclient import TestClient

from app.main import app
from app.users import UsersProcessor
from settings import CONFIG_FILE, CONFIG_FOLDER


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def fake_users_processor(tmp_path):
    base_dir = Path(__file__).parent

    config_template = base_dir / CONFIG_FILE
    path_to_config_folder = base_dir / CONFIG_FOLDER
    config_template_content = config_template.read_text()

    temp_config = tmp_path / config_template.name
    temp_config.write_text(config_template_content)

    return UsersProcessor(config_file=temp_config, config_folder=path_to_config_folder)
