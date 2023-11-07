import logging
import os
import json
from typing import Union


logger = logging.getLogger('app-logger')


def generate_email_map() -> "Union[dict[str, dict], None]":
    """
    Returns a map of lowercased user emails
    to the corresponding user configs.
    """
    path = os.getenv("DIRECTORY_FILE_PATH")
    if path is None:
        logger.error("Env var to user configs not set!")
        return
    logger.info(f"Path to user configs: {path}")
    email_map = {}
    with open(path) as f:
        user_directory: list[dict] = json.load(f)

    for user in user_directory:
        try:
            contact_emails: list[str] = user["general"]["contact_emails"]
            for contact_email in contact_emails:
                contact_email = contact_email.lower()
                email_map[contact_email] = user
        except KeyError as error:
            logger.error(f"Key Error: {error}")

    logger.info(f"email map size: {len(email_map)}")
    return email_map


def load_user_directory():
    path = os.getenv("DIRECTORY_FILE_PATH")
    if path is None:
        logger.error("Env var to user configs not set!")
        return
    logger.info(f"Path to user configs: {path}")
    with open(path) as f:
        user_directory: list[dict] = json.load(f)
    return user_directory
