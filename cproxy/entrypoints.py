#!/usr/bin/env python
# -*- coding: utf-8 -*-

from werkzeug.serving import run_simple
from cproxy import app


def run_werkzeug():
    run_simple('0.0.0.0', 8000, app, use_reloader=True)
