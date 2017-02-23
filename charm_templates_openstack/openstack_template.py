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

import jinja2
import logging
import os
import shutil
import stat
import subprocess

import charmtools.generators

log = logging.getLogger(__name__)


class OpenStackCharmTemplate(charmtools.generators.CharmTemplate):

    # _EXTRA_FILES is the list of names of files present in the git repo
    # we don't want transferred over to the charm template:
    _EXTRA_FILES = ["README.md", ".git", ".gitmodules", "test-artifacts"]
    skip_parsing = ['README.ex', '*.pyc', '*sample']

    def create_charm(self, config, output_dir):
        """Generate charm from template

        :param config: dict Base context for rendering templates
        :param output_dir: str Directory to write charm out to
        """
        self.config = config
        self.output_dir = output_dir
        self.clone_template_repo()
        self.rename_files()
        for root, dirs, files in os.walk(self.output_dir):
            for outfile in files:
                if not self.skip_template(outfile):
                    self.write_template(os.path.join(root, outfile))

    @property
    def template_context(self):
        """Template context"""
        self.config['charm_class'] = '{}Charm'.format(
            self.config['metadata']['package'].title().replace('-', ''))
        self.config['charm_lib'] = self.config['metadata']['package'].replace(
            '-', '_')
        return self.config

    def write_template(self, outfile):
        """Write out template using template_context, preserving file perms

        :param outfile: File to render
        """
        if os.path.islink(outfile):
            return
        mode = os.stat(outfile)[stat.ST_MODE]
        with open(outfile, 'r') as f:
            template_src = f.read()
        template = jinja2.Template(template_src)
        with open(outfile, 'wb') as f:
            os.chmod(outfile, mode)
            f.write(template.render(self.template_context))

    def clone_template_repo(self):
        """Clone Git repository containing templated charm

        """
        templ_url = os.environ.get(
            'CHARM_TEMPLATE_ALT_REPO',
            self._TEMPLATE_URL)
        cmd = "git clone --recursive {} {}".format(
            templ_url, self.output_dir
        )
        subprocess.check_call(cmd.split())

        # iterate and remove all the unwanted files from the git repo:
        for item in [os.path.join(self.output_dir, i)
                     for i in self._EXTRA_FILES]:
            if not os.path.exists(item):
                continue
            if os.path.isdir(item) and not os.path.islink(item):
                shutil.rmtree(item)
            else:
                os.remove(item)

    @property
    def handler_dir(self):
        """Directory containing reactive handler template"""
        return os.path.join(self.output_dir, 'src', 'reactive')

    @property
    def charm_lib_dir(self):
        """Directory containing charm lib module"""
        return os.path.join(self.output_dir, 'src', 'lib', 'charm',
                            'openstack')

    @property
    def unit_test_dir(self):
        """Directory containing the unit tests"""
        return os.path.join(self.output_dir, 'unit_tests')

    @property
    def file_renames(self):
        """Files that require renaming"""
        return [
            {'dirname': self.handler_dir,
             'src_file': self.charm_type + '_charm_handlers.py',
             'dest_file': self.template_context['charm_lib'] + '_handlers.py'},
            {'dirname': self.charm_lib_dir,
             'src_file': self.charm_type + '_charm.py',
             'dest_file': self.template_context['charm_lib'] + '.py'}]

    def rename_files(self):
        """Rename files to charm specific names"""
        for rename_info in self.file_renames:
            os.rename(
                os.path.join(rename_info['dirname'], rename_info['src_file']),
                os.path.join(rename_info['dirname'], rename_info['dest_file']))
