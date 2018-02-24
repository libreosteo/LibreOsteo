############################################################
# Dockerfile to run libreosteo Containers
############################################################

FROM littlejo/libreosteo-common
LABEL maintainer "Joseph Ligier"

ENV version 0.5.7

ENV software Libreosteo
ENV url_base https://codeload.github.com/garthylou/Libreosteo/tar.gz
ENV url $url_base/$version
ENV dir $software-$version

# Download libreosteo
RUN curl $url | tar xvz

# Install libreosteo
WORKDIR /$dir

RUN pip install -r requirements/requ-py2.txt
RUN bower install --allow-root 
RUN python manage.py collectstatic --noinput

COPY launch-libreosteo.sh .
COPY local.py.pg Libreosteo/settings/

# Security: use another user than root
RUN chown -R libreosteo: .
USER libreosteo

EXPOSE 8085

ENTRYPOINT ["bash", "launch-libreosteo.sh"]
