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

log = logging.getLogger(__name__)


class NeutronPluginTemplate(CharmTemplate):
    """Creates a reactive, layered python-based charm"""

    # _EXTRA_FILES is the list of names of files present in the git repo
    # we don't want transferred over to the charm template:
    _EXTRA_FILES = ["README.md", ".git", ".gitmodules"]

    _TEMPLATE_URL = "https://github.com/openstack-charmers/charm-template-neutron-plugin"

    def create_charm(self, config, output_dir):
        self._clone_template(config, output_dir)
        self.prompts()
        charm_initcap = [a.title()
                         for a
                         in config['metadata']['package'].split('-')]
        charm_class = '{}Charm'.format(''.join(charm_initcap))
        config['charm_class'] = charm_class
        config['packages'] = str(config['packages'].split())
        config['release'] = config['release'].lower()
        new_name = config['metadata']['package'].replace('-', '_')
        config['charm_lib'] = '{}'.format(new_name)
        for root, dirs, files in os.walk(output_dir):
            for outfile in files:
                if self.skip_template(outfile):
                    continue

                self._template_file(config, path.join(root, outfile))

    def _template_file(self, config, outfile):
        if path.islink(outfile):
            return

        mode = os.stat(outfile)[ST_MODE]
        t = Template(file=outfile, searchList=(config))
        o = tempfile.NamedTemporaryFile(
            dir=path.dirname(outfile), delete=False)
        os.chmod(o.name, mode)
        o.write(str(t))
        o.close()
        backupname = outfile + str(time.time())
        os.rename(outfile, backupname)
        os.rename(o.name, outfile)
        os.unlink(backupname)

    def _clone_template(self, config, output_dir):
        cmd = "git clone --recursive {} {}".format(
            self._TEMPLATE_URL, output_dir
        )

        try:
            subprocess.check_call(cmd.split())
        except OSError as e:
            raise Exception(
                "The below error has occurred whilst attempting to clone"
                "the charm template. Please make sure you have git"
                "installed on your system.\n" + e
            )

        # iterate and remove all the unwanted files from the git repo:
        for item in [path.join(output_dir, i) for i in self._EXTRA_FILES]:
            if not path.exists(item):
                continue

            if path.isdir(item) and not path.islink(item):
                shutil.rmtree(item)
            else:
                os.remove(item)

        # rename handlers.py to <charm-name>.py
        new_name = config['metadata']['package'].replace('-', '_')
        new_handler_name = '{}_handlers.py'.format(new_name)
        new_lib_name = '{}.py'.format(new_name)
        os.rename(os.path.join(output_dir, 'src', 'reactive', 'sdn_charm_handlers.py'),
                  os.path.join(output_dir, 'src', 'reactive', new_handler_name))
        os.rename(os.path.join(output_dir, 'src', 'lib', 'charm', 'openstack', 'sdn_charm.py'),
                  os.path.join(output_dir, 'src', 'lib', 'charm', 'openstack', new_lib_name))
