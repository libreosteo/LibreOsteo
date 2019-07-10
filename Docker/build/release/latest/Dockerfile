############################################################
# Dockerfile to run libreosteo Containers
############################################################

FROM littlejo/libreosteo-alpine-common

LABEL maintainer "Joseph Ligier"
ENV software Libreosteo
ENV version 0.5.7


ENV debug False
ENV sql_host db
ENV sql_port 5432
ENV sql_name postgres
ENV sql_user postgres

# Download libreosteo
ENV url_base https://codeload.github.com/garthylou/Libreosteo/tar.gz
ENV url $url_base/$version
ADD $url Libreosteo.tar.gz
RUN tar fxvz Libreosteo.tar.gz
RUN mv /Libreosteo-$version /Libreosteo
RUN chown -R libreosteo: /Libreosteo

WORKDIR /Libreosteo

# Install libreosteo
RUN pip install -r requirements/requ-py2.txt
ADD django-secret-key /usr/local/bin/

COPY launch-libreosteo.sh .
RUN chmod a+x launch-libreosteo.sh

USER libreosteo
RUN bower install
RUN python manage.py collectstatic --noinput
COPY local.py.pg Libreosteo/settings/
COPY local.py.sqlite Libreosteo/settings/

VOLUME ["/Libreosteo/media", "/Libreosteo/sql"]

EXPOSE 8085

ENTRYPOINT ["./launch-libreosteo.sh"]
