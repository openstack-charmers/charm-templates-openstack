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

    def update_template_ctxt(self, config):
        charm_initcap = [a.title()
                         for a
                         in config['metadata']['package'].split('-')]
        charm_class = '{}Charm'.format(''.join(charm_initcap))
        config['charm_class'] = charm_class
        config['packages'] = str(config['packages'].split())
        config['release'] = config['release'].lower()
        new_name = config['metadata']['package'].replace('-', '_')
        config['charm_lib'] = '{}'.format(new_name)
        config['service_conf'] = 'apple'
        # there must be a better way of creating a string representation of
        # the restart_map...
        restart_map = {a: 'services' for a in config['service_confs'].split()}
        restart_map = str(restart_map).replace("'services'", "services")
        config['restart_map'] = restart_map
        all_services = 'haproxy {} {}'.format(
            config['api_service'],
            config['service_init'])
        config['all_services'] = str(all_services.split())
        log.info('{}'.format(config['restart_map']))
        bob = []
        for cmd in config['db_sync_command'].split(','):
            bob.append(str(cmd.split()))
        config['db_sync_commands'] = bob
        config['db_sync_command'] = str(config['db_sync_command'].split())
        return config

    def rename_files(self, config, output_dir):
        # rename handlers.py to <charm-name>.py
        new_name = config['metadata']['package'].replace('-', '_')
        new_handler_name = '{}_handlers.py'.format(new_name)
        new_lib_name = '{}.py'.format(new_name)
        os.rename(
            os.path.join(output_dir, 'src', 'reactive',
                         'api_charm_handlers.py'),
            os.path.join(output_dir, 'src', 'reactive', new_handler_name))
        os.rename(
            os.path.join(output_dir, 'src', 'lib', 'charm', 'openstack',
                         'api_charm.py'),
            os.path.join(output_dir, 'src', 'lib', 'charm', 'openstack',
                         new_lib_name))
