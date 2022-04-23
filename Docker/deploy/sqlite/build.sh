DEST_DIR=dist
FILES_TO_INCLUDE="install-libreosteo.sh libreosteo README uninstall-libreosteo.sh"
DIRS_TO_INCLUDE="etc var"
mkdir ${DEST_DIR}
echo "#!/bin/sh" > ${DEST_DIR}/auto_install
echo "echo Auto-install LibreOsteo by CambiaTech" >> ${DEST_DIR}/auto_install
echo "sed -e '1,/^exit$/d' \"\$0\" | tar xzf - && ./install-libreosteo.sh" >> ${DEST_DIR}/auto_install
#echo "sed -e '1,/^exit$/d' \"\$0\" > /tmp/tmp.test" >> ${DEST_DIR}/auto_install
echo "exit" >> ${DEST_DIR}/auto_install
chmod +x ${DEST_DIR}/auto_install
tar -czf - ${FILES_TO_INCLUDE} ${DIRS_TO_INCLUDE} >> ${DEST_DIR}/auto_install
