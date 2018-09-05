#!/bin/bash

CONF_DIR=/etc/libreosteo
LIB_DIR=/var/lib/libreosteo
BIN_DIR=/usr/local/bin

SRC_CONF_DIR=etc/libreosteo
SRC_LIB_DIR=var/lib/libreosteo
SRC_BIN_DIR=.

source var/lib/libreosteo/check

check_root

mkdir -p $CONF_DIR $LIB_DIR

cp -v $SRC_CONF_DIR/* $CONF_DIR/
cp -v $SRC_LIB_DIR/* $LIB_DIR/
cp -v $SRC_BIN_DIR/libreosteo $BIN_DIR/

sed -i "s@$SRC_CONF_DIR@$CONF_DIR@g" $BIN_DIR/libreosteo
sed -i "s@$SRC_LIB_DIR@$LIB_DIR@g" $BIN_DIR/libreosteo
chmod a+x $BIN_DIR/libreosteo
