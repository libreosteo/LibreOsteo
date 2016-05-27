############################################################
# Dockerfile to run libreosteo Containers
# Based on Ubuntu Image
############################################################

# Set the base image to use to Ubuntu
FROM ubuntu

# Set the file maintainer (your name - the file's author)
MAINTAINER Joseph Ligier

ENV version 0.6.dev0
ENV software Libreosteo
ENV dir $software-$version
ENV url_base https://codeload.github.com/garthylou/Libreosteo/tar.gz
ENV url $url_base/$version

# Install dependancies
RUN apt-get update && apt-get install -y \
    curl \
    gettext \
    git \
    npm \
    python-dev \
    python-pip \
 && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/nodejs /usr/bin/node \
 && npm install -g bower

# Download libreosteo
RUN curl $url | tar xvz

# Install libreosteo
WORKDIR /$dir
RUN pip install -r requirements/requ-py2.txt \
 && python manage.py migrate \
 && bower install --allow-root \
 && python manage.py collectstatic --noinput

# Port to expose
EXPOSE 8085

# Default libreosteo run command arguments
CMD ["python", "server.py"]

# Set the user to run libreosteo daemon
USER root
