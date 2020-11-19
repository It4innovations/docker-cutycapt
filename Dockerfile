FROM debian:latest
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get clean && apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

RUN apt-get clean && \
    apt-get update -y && \
    apt-get install -y xfonts-75dpi xfonts-100dpi xfonts-cyrillic xfonts-scalable xvfb \
                       build-essential imagemagick cutycapt netcat curl net-tools \
                       python-pip virtualenv python3-virtualenv python-dev python3-dev

RUN pip install --upgrade pip setuptools
RUN pip install yattag Flask gunicorn requests six pyvirtualdisplay
RUN virtualenv -p python3 /opt/.venv3
RUN . /opt/.venv3/bin/activate && pip install --upgrade pip setuptools
RUN . /opt/.venv3/bin/activate && pip install yattag Flask gunicorn requests six pyvirtualdisplay

WORKDIR /opt/cutycapt

COPY entrypoint.sh .
COPY app.py .
RUN chmod +x app.py

EXPOSE 5000/tcp
ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
