import os
from pathlib import Path

BASE_URL = os.environ.get("BASE_URL", "")
CONFIG_FILE = os.environ.get("CONFIG_FILE", "tests/source/config.cfg")
CONFIG_FOLDER = os.environ.get("CONFIG_FOLDER", "tests/source/configs/")

base_dir = Path(__file__).parent
config_file_path = base_dir / CONFIG_FILE
config_folder_path = base_dir / CONFIG_FOLDER
