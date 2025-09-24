FROM python:3.9.23-alpine

WORKDIR /app

RUN apk --update add imagemagick-dev py-pip

ENV MAGICK_HOME=/usr

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 


COPY . . 

ENV PORT=8080

CMD uvicorn main:app --host 0.0.0.0 --port $PORT
