FROM mongo:4.0.20-xenial AS rucs_db

#RUN /bin/mongo

FROM nginx:stable AS httpd

COPY config/default.conf /etc/nginx/conf.d
COPY index.html /usr/share/nginx/html
COPY index.js /usr/share/nginx/html
COPY index.css /usr/share/nginx/html

FROM python:3.8 AS rucs_api

WORKDIR /pyap1

COPY . ./

RUN pip install -r requirements.txt

RUN mkdir -p instance

COPY config/dev.cfg instance

#RUN ./uwsgi-ini
