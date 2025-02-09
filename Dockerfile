FROM python:3.12

RUN mkdir -p /usr/src
WORKDIR /usr/src

RUN apt-get update && apt-get upgrade -y

COPY ./ /usr/src
COPY telethon.session /usr/src/telethon.session
RUN pip install --upgrade pip && pip install -r requirements.txt