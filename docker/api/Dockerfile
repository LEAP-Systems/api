FROM ubuntu:latest


LABEL author="Christian Sargusingh (cSDes1gn)" 

EXPOSE ${FLASK_PORT} 

WORKDIR /srv

RUN apt update && \
	apt dist-upgrade -y && \
	apt install -y python3 python3-pip

COPY . .

RUN python3 -m pip install -r requirements.txt

CMD [ "flask", "run" , "-h", "0.0.0.0", "-p", "5000"]