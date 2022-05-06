# syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "bot.py"]
