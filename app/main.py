from typing import Union
from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks
import os
from pydantic import BaseModel
import logging
from logging.config import dictConfig
from app.logging.config import log_config
from app.utils import generate_email_map
from app.email import send_email
from dotenv import load_dotenv


@asynccontextmanager
async def lifespan(app: FastAPI):
    # In case we need to do some initial setup
    yield


dictConfig(log_config)
logger = logging.getLogger('app-logger')
secrets_path = os.getenv("SECRETS_PATH")
load_dotenv(secrets_path)
email_to_user = generate_email_map()
app = FastAPI(lifespan=lifespan)


class Email(BaseModel):
    email_address: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/send-edit-link")
async def send_edit_link(email: Email, background_tasks: BackgroundTasks):
    return_msg = (
        "We received your email address and will be sending you an edit"
        " link shortly!"
    )
    email_address = email.email_address.lower()
    if email_address not in email_to_user:
        logger.info(f"email {email_address} not found in directory")
        return return_msg
    user_config = email_to_user[email_address]
    background_tasks.add_task(send_email, user_config, email_address)
    logger.info(f"user config (truncated): {str(user_config)[0:100]}...")
    return return_msg
