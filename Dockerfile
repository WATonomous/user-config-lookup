# Start from the official Python base image
FROM python:3-bullseye

# Set the current working directory to /code
# This is where we'll put the requirements.txt file and the app directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Setup code and data needed for this thing
COPY ./app /code/app

# run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5500"]
