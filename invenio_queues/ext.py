# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Invenio module for collecting statistics."""

from __future__ import absolute_import, print_function

from flask import current_app
from pkg_resources import iter_entry_points
from werkzeug.utils import cached_property

from . import config
from .queue import Queue


class _InvenioQueuesState(object):
    """State object for Invenio queues."""

    def __init__(self, app, connection_pool):
        self.app = app
        self._queues = None
        self.connection_pool = connection_pool

    @cached_property
    def queues(self):
        if self._queues is None:
            self._queues = dict()
            for ep in iter_entry_points(group='invenio_queues.queues'):
                try:
                    for cfg in ep.load()():
                        self._queues[cfg['name']] = \
                            Queue(cfg['exchange'], cfg['name'],
                                  self.connection_pool)
                except Exception:
                    current_app.logger.error(
                        'Failed to declare queue: {0}'.format(ep.name))
                    raise
        return self._queues

    def _action(self, action, event_types=None):
        for q in self.queues:
            getattr(self.queues[q].queue, action)()

    def declare(self, **kwargs):
        """Declare queue for all or specific event types."""
        self._action('declare', **kwargs)

    def delete(self, **kwargs):
        """Delete queue for all or specific event types."""
        self._action('delete', **kwargs)

    def purge(self, **kwargs):
        """Delete queue for all or specific event types."""
        self._action('purge', **kwargs)


class InvenioQueues(object):
    """Invenio-Queues extension."""

    def __init__(self, app=None, **kwargs):
        """Extension initialization."""
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app, entry_point_group='invenio_queues.queues'):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['invenio-queues'] = \
            _InvenioQueuesState(app, app.config['QUEUES_CONNECTION_POOL'])
        return app

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith('QUEUES_'):
                app.config.setdefault(k, getattr(config, k))

    def __getattr__(self, name):
        """Proxy to state object."""
        return getattr(self._state, name, None)
