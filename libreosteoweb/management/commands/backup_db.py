#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from libreosteoweb import models
import libreosteoweb
import zipfile
from io import BytesIO, StringIO


def backup_db(exclude=['contenttypes', 'admin', 'auth.Permission'],
              version=libreosteoweb.__version__):
    zip_wrapper = BytesIO()
    zip_content = zipfile.ZipFile(zip_wrapper, "w")

    buf = StringIO()
    call_command('dumpdata', exclude=exclude, stdout=buf)
    buf.seek(0)

    zip_content.writestr('dump.json', buf.getvalue())

    documents = models.Document.objects.all()

    for document in documents:
        zip_content.write(document.document_file.path,
                          document.document_file.name)

    zip_content.writestr("meta", version)
    zip_content.close()
    return zip_wrapper


class Command(BaseCommand):
    help = 'Make restore.db by CLI'

    def add_arguments(self, parser):
        parser.add_argument('file_name', action='store')

    def handle(self, file_name, **options):
        zf = backup_db()
        open(file_name, 'wb').write(zf.getvalue())
        self.stdout.write(
            self.style.SUCCESS('Backup created into %s' % (file_name, )))
