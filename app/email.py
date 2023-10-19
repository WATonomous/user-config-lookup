import logging
import os
import yaml


logger = logging.getLogger('app-logger')


def send_email(file_path: str):
    user_config = yaml.safe_load(open(file_path))
    logger.debug(f"OPENED FILE: {user_config}")
    return file_path
