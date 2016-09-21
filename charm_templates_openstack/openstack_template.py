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

import stat
import jinja2

from charmtools.generators import (
    CharmTemplate,
    Prompt,
    PromptList,
)

log = logging.getLogger(__name__)


class OpenStackCharmTemplate(CharmTemplate):

    # _EXTRA_FILES is the list of names of files present in the git repo
    # we don't want transferred over to the charm template:
    _EXTRA_FILES = ["README.md", ".git", ".gitmodules"]

    def create_charm(self, config, output_dir):
        self._clone_template(config, output_dir)
        self.rename_files(config, output_dir)
        config = self.update_template_ctxt(config)
        for root, dirs, files in os.walk(output_dir):
            for outfile in files:
                if self.skip_template(outfile):
                    continue

                self._template_file(config, path.join(root, outfile))

    def update_template_ctxt(self, config):
        return config

    def _template_file(self, config, outfile):
        if path.islink(outfile):
            return

        # This is ugly. The template to use is known (its outfile) but there
        # seems to be no way to point jinja directly at a template . Instead it
        # wants to search for it. So extract the directory from outfile and
        # point the jinja2 loader there.
        charm_subdir = os.path.dirname(outfile)
        loaders = [jinja2.FileSystemLoader(charm_subdir)]
        jinja_env = jinja2.Environment(loader=jinja2.ChoiceLoader(loaders))
        template = jinja_env.get_template(os.path.basename(outfile))
        t = template.render(config)
        mode = os.stat(outfile)[stat.ST_MODE]
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

    def rename_files(self, config, output_dir):
        return
