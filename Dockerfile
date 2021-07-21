FROM python:3.6.9-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

COPY deploy.sh ./deploy.sh
RUN chmod u+x deploy.sh

COPY . ./
EXPOSE 8000

ENTRYPOINT ["./deploy.sh"]
