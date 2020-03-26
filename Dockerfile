# Remember to also update .circleci/config.yml
FROM debian:buster
RUN apt-get update
RUN apt-get install -y vim less postgresql-client python3-pip

RUN useradd -m -s /bin/bash app
USER app
ENV PATH=/home/app/.local/bin:/usr/local/bin:/usr/bin:/bin

WORKDIR /home/app/app
ENV PYTHONPATH=/home/app/app
ENV DJANGO_SETTINGS_MODULE=config.settings.dev
COPY --chown=app:app requirements/*.txt requirements/
RUN pip3 install --user --no-warn-script-location -r requirements/dev.txt
