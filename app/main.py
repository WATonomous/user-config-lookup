from typing import Union
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from logging.config import dictConfig
from app.logging.config import log_config
from app.utils import generate_email_map
from app.email import send_email


email_to_file = generate_email_map()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # loop through all emails and map them to a filename
    yield


dictConfig(log_config)
app = FastAPI(lifespan=lifespan, debug=True)


class Email(BaseModel):
    email_address: str


@app.get("/")
def read_root():
    return {"Hello": "OMG"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return str(email_to_file)[0:1000]


@app.post("/send-edit-link")
def send_edit_link(email: Email):
    email_address = email.email_address
    if email_address not in email_to_file:
        return "sus"
    file_path = email_to_file[email_address]
    send_email(file_path)
    return file_path
