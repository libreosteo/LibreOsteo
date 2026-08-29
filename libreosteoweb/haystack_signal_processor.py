# This file is part of LibreOsteo.
#
# LibreOsteo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LibreOsteo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LibreOsteo.  If not, see <http://www.gnu.org/licenses/>.
from haystack.signals import BaseSignalProcessor
from django.db import transaction

class SingleIndexSignalProcessor(BaseSignalProcessor):
    """
    Empêche les indexations multiples lors d'un même cycle de sauvegarde.
    Compatible Whoosh + Haystack.
    """

    def setup(self):
        from django.db.models.signals import post_save, post_delete
        post_save.connect(self.handle_save)
        post_delete.connect(self.handle_delete)

    def teardown(self):
        from django.db.models.signals import post_save, post_delete
        post_save.disconnect(self.handle_save)
        post_delete.disconnect(self.handle_delete)

    def handle_save(self, sender, instance, **kwargs):
        if not self.should_update(sender):
            return

        # Indexation unique par transaction
        transaction.on_commit(lambda: self.handle_update(instance))

    def handle_delete(self, sender, instance, **kwargs):
        if not self.should_update(sender):
            return

        transaction.on_commit(lambda: self.handle_delete(instance))
