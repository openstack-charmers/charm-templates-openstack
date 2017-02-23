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

import charm_templates_openstack.openstack_template as openstack_template

log = logging.getLogger(__name__)


class ManilaPluginTemplate(openstack_template.OpenStackCharmTemplate):
    """Creates a reactive, layered python-based charm"""

    _TEMPLATE_URL = ("https://github.com/openstack-charmers/"
                     "charm-template-manila-plugin.git")
    charm_type = 'manila_plugin'

    @property
    def template_context(self):
        ctxt = super(ManilaPluginTemplate, self).template_context
        ctxt['release'] = ctxt['release'].lower()
        ctxt['version_package'] = ctxt['version-package'].lower()
        ctxt['packages_list'] = "[{}]".format(", ".join(
            [p for p in ctxt['packages'].split(' ')]))
        return ctxt

    @property
    def file_renames(self):
        """Add in the test files to the defaults"""
        return super(ManilaPluginTemplate, self).file_renames + [
            {'dirname': self.unit_test_dir,
             'src_file': 'test_lib_charm_openstack_manila_plugin.py',
             'dest_file': 'test_lib_{}_handlers.py'.format(
                 self.template_context['charm_lib'])},
            {'dirname': self.unit_test_dir,
             'src_file': 'test_manila_plugin_handlers.py',
             'dest_file': 'test_{}_handlers.py'.format(
                 self.template_context['charm_lib'])}]
