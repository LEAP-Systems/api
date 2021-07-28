FROM ubuntu:latest

LABEL author="Christian Sargusingh (cSDes1gn)"

WORKDIR /srv

RUN apt update && \
	apt dist-upgrade -y && \
	apt install -y python3

COPY . .

RUN python3 -m pip install -r requirements.txt
RUN flask run