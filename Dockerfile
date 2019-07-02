FROM python:3.5-alpine
MAINTAINER Kateryna

RUN mkdir /lastfm_analysis
WORKDIR /lastfm_analysis

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 apk add jpeg-dev zlib-dev
COPY requirements.txt requirements.txt

RUN  python3 -m pip install -r requirements.txt --no-cache-dir
RUN apk --purge del .build-deps

COPY . /lastfm_analysis

CMD python manage.py runserver

