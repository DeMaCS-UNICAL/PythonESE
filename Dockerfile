FROM python:3

COPY . .

RUN apt-get update && \
    apt-get install -y bubblewrap && \
    rm -rf /var/lib/apt/lists/*

RUN pip install .

CMD ese-run
