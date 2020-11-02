FROM mongo:4.0.20-xenial AS rucs_db

FROM nginx:stable AS httpd

RUN rm /etc/nginx/conf.d/default.conf
COPY config/httpd_default.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html
COPY index.js /usr/share/nginx/html
COPY index.css /usr/share/nginx/html

FROM python:3.8 AS rucs_api

WORKDIR /pyap1

COPY . ./

RUN pip install -r requirements.txt

RUN mkdir -p instance

# todo: load uwsgi as a systemd service
#COPY uwsgi_rc.local /etc/rc.local

COPY config/dev.cfg instance
