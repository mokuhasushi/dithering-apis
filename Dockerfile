FROM python:3.9.23-alpine

WORKDIR /usr/src/app

RUN apk --update add imagemagick-dev

ENV MAGICK_HOME=/usr

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 

COPY . . 
