############################################################
# Dockerfile to have dependancies to install Libreosteo
# Based on Ubuntu Image
############################################################

FROM ubuntu:16.04
LABEL maintainer "Joseph Ligier"

# Install dependancies
RUN apt-get update && apt-get install -y \
    curl \
    tzdata \
    gettext \
    git \
    npm \
    python-dev \
    python-psycopg2 \
    python-pip

RUN ln -s /usr/bin/nodejs /usr/bin/node \
 && npm install -g bower

RUN git clone https://github.com/libreosteo/Libreosteo.git \
 && pip install -r Libreosteo/requirements/requ-py2.txt \
 && rm -rf /Libreosteo

# Create user
RUN adduser --disabled-password --gecos '' libreosteo
