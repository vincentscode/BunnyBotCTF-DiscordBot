# syntax=docker/dockerfile:1

FROM python:3.10

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

COPY . .

ENTRYPOINT python3 bot.py