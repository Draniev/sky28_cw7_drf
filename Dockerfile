FROM python:3.12

WORKDIR /code

RUN apt-get update && apt-get install
RUN pip install --upgrade pip

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .
