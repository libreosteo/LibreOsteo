#!/bin/bash

/Applications/Libreosteo.app/Contents/MacOS/manage migrate
myuser=${SUDO_USER:-$USER}
chown -R ${myuser} "/Users/${myuser}/Library/Application Support/Libreosteo"