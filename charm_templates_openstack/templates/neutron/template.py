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
import os.path as path
import time
import shutil
import subprocess
import tempfile

from Cheetah.Template import Template
from stat import ST_MODE

from charmtools.generators import (
    CharmTemplate,
)
import charm_templates_openstack.openstack_template as openstack_template

log = logging.getLogger(__name__)


class NeutronPluginTemplate(openstack_template.OpenStackCharmTemplate):
    """Creates a reactive, layered python-based charm"""

    _TEMPLATE_URL = "https://github.com/openstack-charmers/charm-template-neutron-plugin"
    charm_type = 'sdn'

    def update_template_ctxt(self):
        super(NeutronPluginTemplate, self).update_template_ctxt()
        self.config['packages'] = str(self.config['packages'].split())
        self.config['release'] = self.config['release'].lower()

