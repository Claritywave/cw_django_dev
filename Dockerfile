FROM python:3.6.9-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

COPY . ./
EXPOSE 8000
