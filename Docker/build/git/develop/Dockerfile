############################################################
# Dockerfile to run libreosteo Containers
############################################################

FROM littlejo/libreosteo-alpine-common

LABEL maintainer "Joseph Ligier"
ENV version 0.6-dev
ENV software Libreosteo
ENV REPO Libreosteo
ENV USER libreosteo
ENV BRANCH develop
ENV debug False
ENV sql_host db
ENV sql_port 5432
ENV sql_name postgres
ENV sql_user postgres


RUN mkdir /$software && chown libreosteo: /$software

USER libreosteo

# Download libreosteo
ADD https://api.github.com/repos/$USER/$REPO/git/refs/heads/$BRANCH version.json
RUN git clone -b $BRANCH https://github.com/$USER/$REPO.git

# Install libreosteo
WORKDIR /Libreosteo

USER root
RUN pip3 install -r requirements/requirements.txt
ADD django-secret-key /usr/local/bin/

COPY launch-libreosteo.sh .
RUN chmod a+x launch-libreosteo.sh

USER libreosteo
RUN yarn
RUN python manage.py collectstatic --noinput
COPY local.py.pg Libreosteo/settings/
COPY local.py.sqlite Libreosteo/settings/

VOLUME ["/Libreosteo/media", "/Libreosteo/sql"]

EXPOSE 8085

ENTRYPOINT ["./launch-libreosteo.sh"]
