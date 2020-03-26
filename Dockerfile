# Remember to also update .circleci/config.yml
FROM debian:buster
RUN apt-get update
RUN apt-get install -y vim less postgresql-client python3-pip

RUN useradd -m -s /bin/bash app
USER app
WORKDIR /home/app/app

COPY --chown=app:app requirements/*.txt requirements/
RUN pip3 install --user --no-warn-script-location -r requirements/dev.txt
