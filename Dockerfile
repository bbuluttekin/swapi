FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# COPY requirements.txt requirements.txt
COPY . .
RUN pip3 install -r requirements.txt

CMD [ "python3", "src/main.py" ]