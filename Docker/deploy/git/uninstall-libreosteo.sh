#!/bin/bash

CONF_DIR=/etc/libreosteo
LIB_DIR=/var/lib/libreosteo
BIN_DIR=/usr/local/bin

source var/lib/libreosteo/check

check_root

ranks_list=$(libreosteo list)
for rank in $ranks_list
do
    libreosteo remove $rank
done

rm -rvf $CONF_DIR $LIB_DIR
rm -v $BIN_DIR/libreosteo

