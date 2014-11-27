#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Libreosteo.settings")

    import django.core.management
    import django.utils.autoreload

    from django.core.management import execute_from_command_line

    original_function = django.core.management.find_commands

    import pkgutil
    from importlib import import_module
    from django.apps import apps
    from django.utils import six

    from django.db.migrations.loader import MIGRATIONS_MODULE_NAME

    def _load_disk(self):
        """
        Loads the migrations from all INSTALLED_APPS from disk.
        """
        self.disk_migrations = {}
        self.unmigrated_apps = set()
        self.migrated_apps = set()
        for app_config in apps.get_app_configs():
            # Get the migrations module directory
            module_name = self.migrations_module(app_config.label)
            was_loaded = module_name in sys.modules
            try:
                module = import_module(module_name)
            except ImportError as e:
                # I hate doing this, but I don't want to squash other import errors.
                # Might be better to try a directory check directly.
                if "No module named" in str(e) and MIGRATIONS_MODULE_NAME in str(e):
                    self.unmigrated_apps.add(app_config.label)
                    continue
                raise
            else:
                # PY3 will happily import empty dirs as namespaces.
                if not hasattr(module, '__file__'):
                    continue
                # Module is not a package (e.g. migrations.py).
                if not hasattr(module, '__path__'):
                    continue
                # Force a reload if it's already loaded (tests need this)
                if was_loaded:
                    six.moves.reload_module(module)
            self.migrated_apps.add(app_config.label)
            # Issue with that when frozen into an executable
            # List the content of the package
            ### BEGIN OF THE REWRITTEN CODE ###
            migration_names = set()
            for (module_loader, name, ispkg) in pkgutil.iter_modules(module.__path__):
                migration_names.add(name)
            ### END OF THE REWRITTEN CODE ###
            # Load them
            south_style_migrations = False
            for migration_name in migration_names:
                try:
                    migration_module = import_module("%s.%s" % (module_name, migration_name))
                except ImportError as e:
                    # Ignore South import errors, as we're triggering them
                    if "south" in str(e).lower():
                        south_style_migrations = True
                        break
                    raise
                if not hasattr(migration_module, "Migration"):
                    raise BadMigrationError(
                        "Migration %s in app %s has no Migration class" % (migration_name, app_config.label)
                    )
                # Ignore South-style migrations
                if hasattr(migration_module.Migration, "forwards"):
                    south_style_migrations = True
                    break
                self.disk_migrations[app_config.label, migration_name] = migration_module.Migration(migration_name, app_config.label)
            if south_style_migrations:
                self.unmigrated_apps.add(app_config.label)

    def _ask_initial(self, app_label):
        "Should we create an initial migration for the app?"
        # If it was specified on the command line, definitely true
        if app_label in self.specified_apps:
            return True
        # Otherwise, we look to see if it has a migrations module
        # without any Python files in it, apart from __init__.py.
        # Apps from the new app template will have these; the python
        # file check will ensure we skip South ones.
        try:
            app_config = apps.get_app_config(app_label)
        except LookupError: # It's a fake app.
            return self.defaults.get("ask_initial", False)
        migrations_import_path = "%s.%s" % (app_config.name, MIGRATIONS_MODULE_NAME)
        filenames = set()
        try:
            migrations_module = import_module(migrations_import_path)
        except ImportError:
            return self.defaults.get("ask_initial", False)
        else:
            if hasattr(migrations_module, "__file__"):
                for (module_loader, name, ispkg) in pkgutil.iter_modules(migrations_module.__file__):
                    filenames.add(name)
            elif hasattr(migrations_module, "__path__"):
                if len(migrations_module.__path__) > 1:
                    return False
                for (module_loader, name, ispkg) in pkgutil.iter_modules(migrations_module.__path__):
                    filenames.add(name)
            return len(filenames) > 0

    def _find_commands(path):
        """
        Given a path to a management directory, returns a list of all the command
        names that are available.

        Returns an empty list if no commands are defined.
        """
        (head, management_dir) = os.path.split(path)
        if head.endswith(os.path.join('django', 'core')) :
            return """compilemessages createcachetable dbshell shell runfcgi migrate loaddata runfcgi""".split()
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
        from django.db.migrations.loader import MigrationLoader
        from django.db.migrations.questioner import MigrationQuestioner
        original_load_disk = MigrationLoader.load_disk
        original_ask_initial = MigrationQuestioner.ask_initial
        
        MigrationLoader.load_disk = _load_disk
        MigrationQuestioner.ask_initial = _ask_initial
        

    execute_from_command_line(sys.argv)

