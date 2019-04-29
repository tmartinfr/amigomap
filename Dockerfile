# Remember to also update .circleci/config.yml
FROM python:3.7.3-stretch
RUN apt-get update
RUN apt-get install -y vim less postgresql-client

RUN useradd -m -G staff -s /bin/bash app
USER app
ENV PATH=/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

WORKDIR /home/app/app
ENV PYTHONPATH=/home/app/app
ENV DJANGO_SETTINGS_MODULE=config.settings.dev
COPY requirements/*.txt requirements/
RUN pip install -r requirements/dev.txt
