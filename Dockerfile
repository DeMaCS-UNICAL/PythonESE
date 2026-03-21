FROM python:3

COPY . .

RUN apt-get update
RUN apt-get install -y bubblewrap

RUN pip install .

CMD ese-run
