import os
import yaml


def generate_email_map():
    path = "/data"
    email_map = {}
    for file in os.scandir(path):
        user_config = yaml.safe_load(open(file))
        contact_emails = user_config["general"]["contact_emails"]
        for contact_email in contact_emails:
            email_map[contact_email] = os.path.abspath(file)
    return email_map
