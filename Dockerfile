FROM ubuntu:22.04

RUN apt update
RUN apt install python3 python3-pip -y
COPY . .

RUN pip install -r requirements.txt

ARG ARG_LISTENING_PORT
ARG ARG_API_URL
ENV LISTENING_PORT=${ARG_LISTENING_PORT}
ENV API_URL=${ARG_API_URL}

RUN apt-get install bubblewrap

EXPOSE ${LISTENING_PORT}

CMD python3 embasp_server_executor/ese_main.py