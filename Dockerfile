############################################################
# Dockerfile to run libreosteo Containers
# Based on Ubuntu Image
############################################################

# Set the base image to use to Ubuntu
FROM ubuntu

# Set the file maintainer (your name - the file's author)
MAINTAINER Joseph Ligier

ENV version 0.4.9.2
ENV software Libreosteo
ENV dir $software-$version
# Update the default application repository sources list
RUN apt-get update

# Install dependancies
RUN apt-get install -y wget \
                       python-pip \
                       python-dev \
                       cx-freeze \
                       npm \
                       gettext \
                       git
RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN npm install -g bower

# Install libreosteo
RUN wget https://codeload.github.com/garthylou/Libreosteo/tar.gz/v$version -O $software.tar.gz
RUN tar zxf $software.tar.gz
RUN mv $dir $software
RUN sed -i '/cx_freeze==4.3.3/d' $software/requirements.txt
RUN pip install -r $software/requirements.txt
RUN python $software/manage.py migrate
RUN echo "from django.contrib.auth.models import User;User.objects.create_superuser('demo', '', 'demo')" | python $software/manage.py shell
RUN python $software/manage.py compilemessages
RUN cp -a $software/templates .

RUN cd $software && bower install --allow-root

RUN python $software/manage.py collectstatic --noinput

# Port to expose (default: 11211)
EXPOSE 11211 8000 8085

# Default libreosteo run command arguments
CMD ["python", "Libreosteo/server.py"]

# Set the user to run libreosteo daemon
USER root
