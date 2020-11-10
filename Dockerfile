FROM python:3.8

WORKDIR /usr/src

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /usr/lib/rucs-api-instance
COPY config/dev.cfg /usr/lib/rucs-api-instance

RUN mkdir -p /var/cache/py
RUN mkdir -p /var/cache/pytest

VOLUME /usr/lib/rucs-api-instance

# todo: load uwsgi as a systemd service - to replace entrypoint?
# COPY uwsgi_rc.local /etc/rc.local
