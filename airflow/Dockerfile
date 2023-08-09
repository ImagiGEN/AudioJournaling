FROM apache/airflow:2.6.1
USER root
RUN apt-get update && apt-get install -y --no-install-recommends wget unzip build-essential libopenmpi-dev && apt-get autoremove -yqq --purge && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN apt-get -y install gcc
# RUN apt install ffmpeg
RUN apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /
COPY keys /opt/airflow/keys
RUN chown -R airflow /opt/airflow/keys
RUN chmod -R 755 /opt/airflow/keys
USER airflow
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt