#!/usr/bin/python
#
#    Copyright (C) 2014  Canonical Ltd.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os

import charm_templates_openstack.openstack_template as openstack_template

log = logging.getLogger(__name__)


class APITemplate(openstack_template.OpenStackCharmTemplate):
    """Creates a reactive, layered python-based charm"""

    _TEMPLATE_URL = "https://github.com/openstack-charmers/charm-template-api.git"
    charm_type = 'api'

    def update_template_ctxt(self):
        super(APITemplate, self).update_template_ctxt()
        # XXX Temporary fix for xenial + hacluster lacking python-apt
        _pkgs = '{} {}'.format(self.config['packages'], 'python-apt')
        self.config['packages'] = str(_pkgs.split())
        self.config['release'] = self.config['release'].lower()
        self.config['service_conf'] = 'apple'
        # There must be a better way of creating a string representation of
        # the restart_map...
        restart_map = {a: 'services'
                       for a in self.config['service_confs'].split()}
        restart_map = str(restart_map).replace("'services'", "services")
        self.config['restart_map'] = restart_map
        all_services = 'haproxy {} {}'.format(
            self.config['api_service'],
            self.config['service_init'])
        self.config['all_services'] = str(all_services.split())
        log.info('{}'.format(self.config['restart_map']))
        sync_commands = []
        for cmd in self.config['db_sync_command'].split(','):
            sync_commands.append(str(cmd.split()))
        self.config['db_sync_commands'] = sync_commands
        self.config['db_sync_command'] = str(
            self.config['db_sync_command'].split())
