############################################################
# Dockerfile to run libreosteo Containers
############################################################

FROM littlejo/libreosteo-alpine-common

LABEL maintainer "Joseph Ligier"
ENV version 0.6-dev
ENV software Libreosteo

RUN mkdir /$software && chown libreosteo: /$software

USER libreosteo
# Download libreosteo
RUN git clone -b develop https://github.com/libreosteo/Libreosteo.git

# Install libreosteo
WORKDIR /Libreosteo

USER root
RUN sed -i 's/cherrypy/cherrypy==10.2.2/' requirements/requirements.txt
RUN pip install -r requirements/requ-py2.txt

COPY launch-libreosteo.sh .
RUN chmod a+x launch-libreosteo.sh

USER libreosteo
RUN bower install
RUN python manage.py collectstatic --noinput
COPY local.py.pg Libreosteo/settings/
COPY local.py.sqlite Libreosteo/settings/
USER libreosteo

VOLUME ["/Libreosteo/media", "/Libreosteo/sql"]

EXPOSE 8085

ENTRYPOINT ["./launch-libreosteo.sh"]
