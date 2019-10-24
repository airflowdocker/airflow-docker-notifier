FROM python:3.7.4

WORKDIR /opt/airflow-docker/notifier/

COPY deps/requirements.txt /opt/airflow-docker/notifier/deps/requirements.txt
RUN pip install -r /opt/airflow-docker/notifier/deps/requirements.txt

COPY . /opt/airflow-docker/notifier/

RUN pip install .

ENTRYPOINT ["airflow-docker-notifier"]
