############################################################
# Dockerfile to run libreosteo Containers
############################################################

FROM littlejo/libreosteo-common

LABEL maintainer "Joseph Ligier"
ENV version 0.6-dev
ENV software Libreosteo

RUN mkdir /$software && chown libreosteo: /$software

USER libreosteo
# Download libreosteo
RUN git clone https://github.com/libreosteo/Libreosteo.git

# Install libreosteo
WORKDIR /Libreosteo

RUN git checkout develop
USER root
RUN pip install -r requirements/requ-py2.txt

USER libreosteo
RUN bower install
RUN python manage.py collectstatic --noinput
COPY launch-libreosteo.sh .
COPY local.py.pg Libreosteo/settings/
COPY local.py.sqlite Libreosteo/settings/

VOLUME ["/Libreosteo/media", "/Libreosteo/sql"]

EXPOSE 8085

ENTRYPOINT ["bash", "launch-libreosteo.sh"]
