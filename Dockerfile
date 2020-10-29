FROM nginx:stable AS httpd

COPY config/default.conf /etc/nginx/conf.d
COPY config/index /usr/share/NGINX/html

#EXPOSE 3031

FROM python:3.8 AS pyap1

WORKDIR /pyap1

COPY requirements.txt .

RUN pip install -r requirements.txt

FROM mongo:4.0.20-xenial AS house_state_db
