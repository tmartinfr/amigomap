# Remember to also update .circleci/config.yml
FROM python:3.7.3-stretch
RUN apt-get update
RUN apt-get install -y vim less postgresql-client

RUN useradd -m -s /bin/bash app
USER app
ENV PATH=/home/app/.local/bin:/usr/local/bin:/usr/bin:/bin

WORKDIR /home/app/app
ENV PYTHONPATH=/home/app/app
ENV DJANGO_SETTINGS_MODULE=config.settings.dev
COPY --chown=app:app requirements/*.txt requirements/
RUN pip install --user -r requirements/dev.txt
