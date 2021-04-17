FROM python:3.6.8-alpine3.9

LABEL MAINTAINER="Don Dayley <example@domain.com>"

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/

ADD . /var/www/
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN pip install boto
RUN pip install configparser
#RUN sudo apt-get install python3.6-dev
#RUN sudo apt install uwsgi uwsgi-plugin-python3
RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

USER www

EXPOSE 5000

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi"]

#CMD [ "uwsgi", "--ini", "app.ini" ]