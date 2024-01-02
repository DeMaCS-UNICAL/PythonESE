FROM ubuntu:22.04

RUN apt update
RUN apt install python3 python3-pip -y
COPY . .

RUN pip install -r requirements.txt

RUN apt-get install bubblewrap

CMD python3 embasp_server_executor/ese_main.py