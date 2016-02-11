#!/bin/bash

/Applications/Libreosteo.app/Contents/MacOS/manage migrate
myuser=${SUDO_USER:-$USER}
chown -R ${myuser} "/Users/${myuser}/Library/Application Support/Libreosteo"
cp /Applications/Libreosteo.app/Contents/Resources/macos/org.libreosteo.macos.Libreosteo.plist "/Users/${myuser}/Library/LaunchAgents/."
chmod +x "/Users/${myuser}/Library/LaunchAgents/org.libreosteo.macos.Libreosteo.plist"
chown -R ${myuser} "/Users/${myuser}/Library/LaunchAgents/org.libreosteo.macos.Libreosteo.plist"
sudo -u ${myuser} launchctl load "/Users/${myuser}/Library/LaunchAgents/org.libreosteo.macos.Libreosteo.plist"
sudo -u ${myuser} launchctl start org.libreosteo.macos.Libreosteo