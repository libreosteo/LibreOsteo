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
# -*- coding: utf-8 -*-

import django.dispatch


from haystack.signals import RealtimeSignalProcessor
import logging

logger = logging.getLogger(__name__)

post_reload_db = django.dispatch.Signal()


class SafeRealtimeSignalProcessor(RealtimeSignalProcessor):
    """
    Signal processor Haystack qui ignore les sauvegardes raw=True
    (cas des loaddata, fixtures, etc.).
    """

    def handle_save(self, sender, instance, **kwargs):
        # Django loaddata passe raw=True → on n'indexe pas
        if kwargs.get("raw"):
            return
        return super().handle_save(sender, instance, **kwargs)

    def handle_delete(self, sender, instance, **kwargs):
        # Même logique si tu veux être cohérent sur les deletes raw
        if kwargs.get("raw"):
            return
        return super().handle_delete(sender, instance, **kwargs)
