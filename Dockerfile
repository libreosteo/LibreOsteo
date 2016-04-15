############################################################
# Dockerfile to run libreosteo Containers
# Based on Ubuntu Image
############################################################

# Set the base image to use to Ubuntu
FROM ubuntu

# Set the file maintainer (your name - the file's author)
MAINTAINER Joseph Ligier

ENV version 0.4.9.1
ENV software Libreosteo
ENV dir $software-$version

# Login password to connect to Libreosteo
ENV login demo
ENV password demo

# Update the default application repository sources list
RUN apt-get update

# Install dependancies
RUN apt-get install -y wget \
                       python-pip \
                       python-dev \
                       npm \
                       gettext \
                       git
RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN npm install -g bower

# Install libreosteo
RUN wget https://codeload.github.com/garthylou/Libreosteo/tar.gz/$version -O $software.tar.gz
RUN tar zxf $software.tar.gz
RUN mv $dir $software
RUN pip install -r $software/requirements/requ-py2.txt
RUN python $software/manage.py migrate
RUN echo "from django.contrib.auth.models import User;User.objects.create_superuser('$login', '', '$password')" | python $software/manage.py shell
RUN python $software/manage.py compilemessages
RUN cp -a $software/templates .

RUN cd $software && bower install --allow-root
RUN python $software/manage.py collectstatic --noinput

# Port to expose
EXPOSE 8085

# Default libreosteo run command arguments
CMD ["python", "Libreosteo/server.py"]

# Set the user to run libreosteo daemon
USER root
