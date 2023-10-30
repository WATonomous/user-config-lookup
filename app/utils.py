import logging
import os
import yaml
from typing import Union


logger = logging.getLogger('app-logger')


def generate_email_map() -> Union[dict, None]:
    """
    returns a map of lowercased user emails
    to the corresponding file path where their 
    user config yml file is
    """
    path = os.getenv("DIRECTORY_PATH")
    if path is None:
        logger.error("Env var to user configs not set!")
        return
    logger.info(f"Path to user configs: {path}")
    email_map = {}
    for file in os.scandir(path):
        if os.path.isdir(file):
            logger.warn(f"Skipping folder at path: {path}")
            continue
        user_config = yaml.safe_load(open(file))
        contact_emails: list[str] = user_config["general"]["contact_emails"]
        for contact_email in contact_emails:
            contact_email = contact_email.lower()
            email_map[contact_email] = os.path.abspath(file)
    logger.info(f"email map size: {len(email_map)}")
    return email_map
