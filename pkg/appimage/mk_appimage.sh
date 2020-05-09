#!/bin/bash

set -x
set -e

# requirements
#   yarn
#   rsync
#   git

# building in temporary directory to keep system clean
# use RAM disk if possible (as in: not building on CI system like Travis, and RAM disk is available)
if [ "$CI" == "" ] && [ -d /dev/shm ]; then
    TEMP_BASE=/dev/shm
else
    TEMP_BASE=/tmp
fi

export VERSION=develop-$(git rev-parse --short HEAD)
BUILD_DIR=$(mktemp -d -p "$TEMP_BASE" appimage-build-XXXXXX)
APP_DIR="$BUILD_DIR/AppDir"
mkdir $APP_DIR

# make sure to clean up build dir, even if errors occur
cleanup () {
    if [ -d "$BUILD_DIR" ]; then
        rm -rf "$BUILD_DIR"
    fi
}
trap cleanup EXIT

# Store repo root as variable
REPO_ROOT=$(dirname $(dirname  $(dirname $(realpath $0))))
OLD_CWD=$(readlink -f .)

# switch to build dir
pushd "$BUILD_DIR"

# Fetch a python relocatable installation
wget -c https://github.com/niess/python-appimage/releases/download/python3.7/python3.7.7-cp37-cp37m-manylinux1_x86_64.AppImage
chmod +x python*.AppImage
./python3.7.7-cp37-cp37m-manylinux1_x86_64.AppImage --appimage-extract

mv squashfs-root/usr $APP_DIR/usr
mv squashfs-root/opt $APP_DIR/opt
rm -rf squashfs-root/

# Pack required source code into AppDir
# Avoid using .git and other unrequired stuff
rsync -av "$REPO_ROOT/" "$APP_DIR/src" \
      --exclude '.git/' \
      --exclude-from="$REPO_ROOT/.gitignore"

# Install requirements (JS and Python)
pushd $APP_DIR

./usr/bin/python3 -m pip install -r src/requirements/requirements.txt
yarn --cwd "$REPO_ROOT"
./usr/bin/python3 src/manage.py collectstatic --no-input

mkdir -p usr/share/metainfo
mv src/pkg/libreosteo.metainfo.xml usr/share/metainfo/

popd


# Get commit version from repository
pushd $REPO_ROOT
export VERSION=develop-$(git rev-parse --short HEAD)
popd


# Now, build AppImage using linuxdeploy
export ARCH=x86_64
wget -c https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
chmod +x linuxdeploy*.AppImage
./linuxdeploy-x86_64.AppImage \
  --appdir $APP_DIR \
  --icon-file $APP_DIR/src/libreosteoweb/static/images/libreosteo.png \
  --desktop-file $APP_DIR/src/pkg/libreosteo.desktop \
  --custom-apprun $APP_DIR/src/pkg/appimage/AppRun \
  --output appimage

# move built AppImage back into original CWD
mv LibreOsteo*.AppImage "$OLD_CWD/"
echo 'Hello LibreOsteo*.Appimage !'
