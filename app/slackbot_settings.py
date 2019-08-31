#!/usr/bin/python
""" Settings module
"""

import yaml
from app.runbot import CONFIG
with open(CONFIG, 'r') as yml:
    CONF = yaml.load(yml.read(), Loader=yaml.FullLoader)

DEFAULT_REPLY = "I'm sorry, Dave, I'm afraid I can't do that."

API_TOKEN = CONF['API_TOKEN']

PLUGINS = ['plugins']
