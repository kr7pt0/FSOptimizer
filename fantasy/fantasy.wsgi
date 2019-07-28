#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FSOptimizer/fantasy/")

from fantasy import app as application
application.secret_key = ''
active_this='/var/ww/FSOptimizer/fantasy/fantasy/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))