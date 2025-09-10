FROM python:3.9.23-alpine

WORKDIR /app

RUN apk --update add imagemagick-dev py-pip

ENV MAGICK_HOME=/usr

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 


COPY . . 

COPY ./scripts/start-web ./start-web
RUN chmod +x ./start-web

COPY ./scripts/start-worker ./start-worker
RUN chmod +x ./start-worker
