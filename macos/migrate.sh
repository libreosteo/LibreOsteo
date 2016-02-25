#!/bin/bash

/Applications/Libreosteo.app/Contents/MacOS/manage migrate
myuser=${SUDO_USER:-$USER}
chown -R ${myuser} "/Users/${myuser}/Library/Application Support/Libreosteo"
cp /Applications/Libreosteo.app/Contents/Resources/macos/org.libreosteo.macos.Libreosteo.plist "/Library/LaunchAgents/."
chmod +x "/Library/LaunchAgents/org.libreosteo.macos.Libreosteo.plist"
sudo launchctl load "/Library/LaunchAgents/org.libreosteo.macos.Libreosteo.plist"
sudo launchctl start org.libreosteo.macos.Libreosteo
