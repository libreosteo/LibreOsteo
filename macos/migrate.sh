#!/bin/bash

/Applications/Libreosteo.app/Contents/MacOS/manage migrate
myuser=${SUDO_USER:-$USER}
chown -R ${myuser} "/Users/${myuser}/Library/Application Support/Libreosteo"
cp /Applications/Libreosteo.app/Contents/Resources/macos/org.libreosteo.macos.Libreosteo.plist "/Library/LaunchDaemons/."
chmod +x "/Library/LaunchDaemons/org.libreosteo.macos.Libreosteo.plist"
sudo launchctl load -w "/Library/LaunchDaemons/org.libreosteo.macos.Libreosteo.plist"
sudo launchctl start org.libreosteo.macos.Libreosteo
