FROM python:3

COPY . .

RUN apt-get install bubblewrap

RUN pip install .

CMD ese-run