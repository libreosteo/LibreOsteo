#!/bin/bash

/Applications/Libreosteo.app/Contents/MacOS/manage migrate
myuser=${SUDO_USER:-$USER}
chown -R ${myuser} "/Users/${myuser}/Library/Application Support/Libreosteo"
agents_dir="/Users/${myuser}/Library/LaunchAgents"
mkdir -p ${agents_dir}
cp /Applications/Libreosteo.app/Contents/Resources/macos/org.libreosteo.macos.Libreosteo.plist ${agents_dir}/.
chmod +x "${agents_dir}/org.libreosteo.macos.Libreosteo.plist"
sudo launchctl load -w "${agents_dir}/org.libreosteo.macos.Libreosteo.plist"
sudo launchctl start org.libreosteo.macos.Libreosteo
