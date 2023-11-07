import logging
import yaml
import json
import os
import aiosmtplib
from urllib.parse import quote
from email.message import EmailMessage
from app.constants import user_directory


logger = logging.getLogger('app-logger')


def generate_edit_link(user_config: dict) -> str:
    config_json_string = json.dumps(user_config)
    config_json_string_encoded = quote(config_json_string)
    base_url = "https://watonomous.github.io/infra-config/onboarding-form"
    edit_link = f"{base_url}/?initialFormData={config_json_string_encoded}"
    logger.debug(f"Edit link (truncated): {edit_link[0:100]}...")

    return edit_link


def generate_email_content(edit_link: str):
    return f"Sent via aiosmtplib! Here's your edit link: {edit_link}"


async def send_email(user_config: dict, email_address: str) -> None:
    edit_link = generate_edit_link(user_config)

    message = EmailMessage()
    message["From"] = "onboarding-noreply@watonomous.ca"
    message["To"] = email_address
    message["Subject"] = "Hello World!"
    message.set_content(generate_email_content(edit_link))

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
