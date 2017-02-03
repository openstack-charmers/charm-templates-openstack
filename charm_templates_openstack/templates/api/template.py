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

    @property
    def template_context(self):
        ctxt = super(APITemplate, self).template_context
        # XXX Temporary fix for xenial + hacluster lacking python-apt
        pkgs = ctxt['packages'].split() + ['python-apt']
        ctxt['all_packages'] = str(pkgs)
        ctxt['release'] = ctxt['release'].lower()
        ctxt['restart_configs'] = ctxt['service_confs'].split()

        all_services = list(set(['haproxy',
                                 ctxt['api_service'],
                                 ctxt['service_init']]))
        ctxt['all_services'] = str(all_services)

        ctxt['db_manage_cmds'] = []
        for cmd in ctxt['db_sync_command'].split(','):
            ctxt['db_manage_cmds'].append(str(cmd.split()))
        ctxt['db_manage_cmd'] = ctxt['db_manage_cmds'][0]
        return ctxt
