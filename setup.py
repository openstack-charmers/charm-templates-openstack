#!/usr/bin/env python

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = ['charm-tools']

setup(name='charm_templates_openstack',
      version='0.0.1.dev1',
      description='charm_templates_openstack',
      long_description=README + '\n\n' + CHANGES,
      license='Apache License 2.0',
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        ],
      author='Liam Young',
      author_email='liam.young@canonical.com',
      url='https://github.com/gnuoy/charm_templates_openstack',
      packages=find_packages(
          exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      include_package_data=True,
      install_requires=requires,
      zip_safe = False,
      entry_points={
        'charmtools.templates': [
           'openstack-api = '
               'charm_templates_openstack.templates.api:APITemplate',
           'openstack-neutron-plugin = '
               'charm_templates_openstack.templates.neutron:NeutronPluginTemplate']})
