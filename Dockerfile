
# This file is part of Libreosteo.
#
# Libreosteo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Libreosteo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Libreosteo.  If not, see <http://www.gnu.org/licenses/>.
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
