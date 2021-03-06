# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 CERN.
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

"""Module tests."""

from __future__ import absolute_import, print_function

from click.testing import CliRunner
from flask.cli import ScriptInfo
from invenio_queues.cli import queues


def test_init(queues_app):
    with queues_app.app_context():
        runner = CliRunner()
        script_info = ScriptInfo(create_app=lambda info: queues_app)
        result = runner.invoke(
            queues, ['init'], obj=script_info)
        assert result.exit_code == 0


def test_purge(queues_app):
    with queues_app.app_context():
        runner = CliRunner()
        script_info = ScriptInfo(create_app=lambda info: queues_app)
        result = runner.invoke(
            queues, ['purge'], obj=script_info)
        assert result.exit_code == 0


def test_delete(queues_app):
    with queues_app.app_context():
        runner = CliRunner()
        script_info = ScriptInfo(create_app=lambda info: queues_app)
        result = runner.invoke(
            queues, ['delete'], obj=script_info)
        assert result.exit_code == 0
