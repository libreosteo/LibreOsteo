############################################################
# Dockerfile to have dependancies to install Libreosteo
# Based on Alpine Image
############################################################

FROM alpine:3.6
LABEL maintainer "Joseph Ligier"

ENV REPO Libreosteo
ENV USER libreosteo
ENV BRANCH develop

# Install dependancies
RUN apk add --no-cache \
    tzdata \
    gettext \
    git \
    python2-dev \
    nodejs \
    nodejs-npm \
    gcc \
    libc-dev \
    linux-headers \
    py2-pip

RUN adduser -S -g '' libreosteo -u 1000
RUN npm install -g bower

ADD https://api.github.com/repos/$USER/$REPO/git/refs/heads/$BRANCH version.json
RUN git clone -b $BRANCH https://github.com/$USER/$REPO.git

RUN pip install -r Libreosteo/requirements/requ-py2.txt
RUN rm -rf /Libreosteo

