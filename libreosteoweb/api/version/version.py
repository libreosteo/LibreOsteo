import urllib.request
import json
import logging
import libreosteoweb
from packaging.version import parse

logger = logging.getLogger()


def ask_for_new_version():
    try:
        logger.info("Ask for new version")
        contents = urllib.request.urlopen(
            "http://libreosteo.github.io/api/version")
        version = json.load(contents)
        logger.info("version read = %s " % version['version'])
        if parse(version['version']) > parse(libreosteoweb.__version__):
            return (True, version['version'])
    except Exception as ex:
        logger.error("Cannot access to version checking", ex)
    return (False, None)
