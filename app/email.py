from email.mime.text import MIMEText
import logging
import json
import os
import aiosmtplib
from urllib.parse import quote
from email.message import EmailMessage


logger = logging.getLogger('app-logger')


def generate_edit_link(user_config: dict) -> str:
    config_json_string = json.dumps(user_config)
    config_json_string_encoded = quote(config_json_string)
    base_url = "https://watonomous.github.io/infra-config/onboarding-form"
    edit_link = f"{base_url}/?initialFormData={config_json_string_encoded}"
    logger.debug(f"Edit link (truncated): {edit_link[0:100]}...")

    return edit_link


def generate_email_content(edit_link: str, user_config: dict):
    name: str = user_config.get("general", {}).get("name")
    if name is None:
        name = "WATcloud user"
    first_name:str = name.split(" ")[0]

    email_body = (
        f"<html>"
        f"<head></head>"
        f"<body><p>"
        f"Hello {first_name},<br><br>" 
        f"As requested, here is the link to edit your WATcloud user config:<br>"
        f"<a href=\"{edit_link}\">Edit Link</a><br><br>"
        f"Thanks,<br>"
        f"WATcloud Team.<br>"
        f"</p></body>"
        f"<html>"
    )
    # return f"Sent via aiosmtplib! Here's your edit link: {edit_link}"
    return email_body


async def send_email(user_config: dict, email_address: str) -> None:
    edit_link = generate_edit_link(user_config)

    message = EmailMessage()
    message["From"] = "onboarding-noreply@watonomous.ca"
    message["To"] = email_address
    message["Subject"] = "WATcloud User Config Edit Link"
    message.set_content(generate_email_content(edit_link, user_config), subtype='html')

    username = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    if username is None or password is None:
        logger.error("environent variables for email credentials not set!")
        return
    
    await aiosmtplib.send(
        message, 
        hostname="smtp.gmail.com", 
        port=587,
        username=username,
        password=password
    )
