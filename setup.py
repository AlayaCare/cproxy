#!/usr/bin/env python

from setuptools import setup

deps = [r.strip() for r in open('requirements.txt').readlines()]


setup(name='cproxy',
      version='0.1',
      description='Simple python http proxy providing signals to hook in custom'
                  ' handlers on the request and response.',
      author='Scott Wilson',
      author_email='scott.wilson@alayacare.com',
      packages=['cproxy'],
      entry_points = {
          'console_scripts': ['cproxy-werkzeug=cproxy.entrypoints:run_werkzeug'],
          },
      scripts = ['scripts/cproxy-gunicorn'],
      install_requires = deps,
      )
