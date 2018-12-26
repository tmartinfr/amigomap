FROM debian:stretch
RUN apt-get update
RUN apt-get install -y vim less postgresql-client
RUN apt-get install -y wget xz-utils build-essential zlib1g-dev libffi-dev libssl-dev

RUN useradd -m -G staff -s /bin/bash app
USER app
ENV PATH=/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

WORKDIR /tmp
RUN wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz
RUN echo "df6ec36011808205beda239c72f947cb Python-3.7.2.tar.xz" | md5sum -c
RUN tar xf Python-3.7.2.tar.xz
RUN cd Python-3.7.2 && ./configure --prefix=/usr/local && make && make install

WORKDIR /home/app/app
ENV PATH=/home/app/.local/bin:$PATH
ENV PYTHONPATH=/home/app/app:/home/app/.local/lib/python2.7/site-packages
ENV DJANGO_SETTINGS_MODULE=config.settings.dev
COPY requirements/*.txt requirements/
RUN pip3 install --user -r requirements/dev.txt
