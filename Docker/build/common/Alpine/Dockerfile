############################################################
# Dockerfile to have dependancies to install Libreosteo
# Based on Alpine Image
############################################################

FROM alpine:3.6
LABEL maintainer "Joseph Ligier"

# Install dependancies
RUN apk add --no-cache \
    tzdata \
    gettext \
    git \
    python2-dev \
    nodejs \
    nodejs-npm \
    gcc \
    libc-dev \
    py2-pip

RUN adduser -S -g '' libreosteo -u 1000

RUN npm install -g bower

RUN git clone -b develop https://github.com/libreosteo/Libreosteo.git
RUN pip install -r Libreosteo/requirements/requ-py2.txt
RUN rm -rf /Libreosteo

