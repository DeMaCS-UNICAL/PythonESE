FROM python:3

COPY . .

ARG APP_VERSION
ENV SETUPTOOLS_SCM_PRETEND_VERSION=${APP_VERSION}

RUN apt-get update && \
    apt-get install -y bubblewrap && \
    rm -rf /var/lib/apt/lists/*

RUN pip install .

CMD ["ese-run"]
