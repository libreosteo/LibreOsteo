#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Libreosteo.settings")

    import django.core.management
    import django.utils.autoreload

    from django.core.management import execute_from_command_line

    original_function = django.core.management.find_commands

    def _find_commands(path):
        """
        Given a path to a management directory, returns a list of all the command
        names that are available.

        Returns an empty list if no commands are defined.
        """
        (head, management_dir) = os.path.split(path)
        if head.endswith(os.path.join('django', 'core')) :
            return """compilemessages createcachetable dbshell shell runfcgi migrate runfcgi""".split()
        elif head.endswith(os.path.join('django', 'contrib', 'staticfiles')):
            return ["runserver",]
        elif head.endswith(os.path.join('django','contrib','auth')):
            return """changepassword createsuperuser""".split()
        else :
            return []


    old_restart_with_reloader = django.utils.autoreload.restart_with_reloader
    def _restart_with_reloader(*args):
        a0 = sys.argv.pop(0)
        try:
            return old_restart_with_reloader(*args)
        finally:
            sys.argv.insert(0, a0)

    if getattr(sys, 'frozen', False):
        # The application is frozen
        django.core.management.find_commands = _find_commands
        django.utils.autoreload.restart_with_reloader = _restart_with_reloader

    execute_from_command_line(sys.argv)

