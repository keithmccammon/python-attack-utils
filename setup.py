#!/usr/bin/env python

from setuptools import setup, find_packages
import os


def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
  name='python-attack-utils',
  author='Keith McCammon',
  author_email='keith@mccammon.org',
  url='https://github.com/keithmccammon/python-attack-utils',
  license='MIT',
  packages=find_packages(),
  description='Python. MITRE ATT&CK(TM)',
  version='0.1',
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: Freely Distributable',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
  ],
  install_requires=[
    'stix2',
    'taxii2-client'
  ],
)
