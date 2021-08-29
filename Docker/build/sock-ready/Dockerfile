############################################################
# Dockerfile to have dependancies to install Libreosteo
# Based on Alpine Image
############################################################

FROM alpine:latest as build
LABEL maintainer="LibreOsteo Team <contact@libreosteo.org>"

ENV VIRTUAL_ENV=/Libreosteo/venv
VOLUME /Libreosteo/data
VOLUME /Libreosteo/settings
VOLUME /Libreosteo/node_modules

# Install dependancies
WORKDIR /Libreosteo
RUN apk add --no-cache \
    tzdata \
    gettext \
    python3-dev \
    py3-pip \
    nodejs \
    gcc \
    libc-dev \
    linux-headers\
    curl\
    bash\
    git \
    nodejs \
    npm && npm install fs path
RUN curl -o - -L https://yarnpkg.com/install.sh | bash -s -- --version 1.21.1


COPY ./requirements ./requirements
COPY ./package.json .
COPY ./libreosteoweb ./libreosteoweb
COPY ./Libreosteo ./Libreosteo
COPY ./locale ./locale
COPY ./zipcode_lookup ./zipcode_lookup
COPY ./templates ./templates
COPY ./manage.py .
COPY ./server.py .

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:/root/.yarn/bin:$PATH"
RUN rm libreosteoweb/static/components || true && . venv/bin/activate && pip3 install -r requirements/requirements.txt && yarn && python3 ./manage.py collectstatic --no-input --settings=Libreosteo.settings.container && python3 ./manage.py compilejsi18n && python3 ./manage.py compress --force --settings=Libreosteo.settings.container
RUN rm libreosteoweb/static/components


FROM alpine:latest as run
LABEL maintainer="LibreOsteo Team <contact@libreosteo.org>"
COPY --from=build /Libreosteo ./Libreosteo
VOLUME /Libreosteo/data
VOLUME /Libreosteo/settings
VOLUME /var/application/static
ENV VIRTUAL_ENV=/Libreosteo/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR /Libreosteo
# Install dependancies
RUN apk add --no-cache \
    tzdata \
    gettext \
    python3-dev \
    py3-pip \
    gcc \
    libc-dev \
    linux-headers\
    postgresql-libs\
    && apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev\
    && pip install uwsgi psycopg2\
    && apk --purge del .build-deps


EXPOSE 3031
CMD python3 ./manage.py migrate --settings=Libreosteo.settings.container \
                                           && python3 ./manage.py import_zipcodes --settings=Libreosteo.settings.container || test 1=1\
                                           && cp -r /Libreosteo/static/. /var/application/static/. \
                                           && export DJANGO_SETTINGS_MODULE=Libreosteo.settings.container \
                                           && uwsgi --socket=:3031 --module Libreosteo.wsgi --master --processes 1 --threads 2 -H /Libreosteo/venv
