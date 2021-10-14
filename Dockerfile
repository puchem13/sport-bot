FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
COPY bot.py bot.py
RUN pip3 install -r requirements.txt

CMD [ "python3", "bot.py" ]
