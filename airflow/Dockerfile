FROM apache/airflow:2.6.1
USER root
# RUN apt-get update && apt-get -y upgrade
RUN apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /
COPY /keys/gkey.json /
USER airflow
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt