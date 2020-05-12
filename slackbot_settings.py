#!/usr/bin/env python

import yaml
from runbot import CONFIG
with open(CONFIG, 'r') as yml:
    config = yaml.load(yml.read(), Loader=yaml.FullLoader)

default_reply = "I'm sorry, Dave, I'm afraid I can't do that."

API_TOKEN = config['API_TOKEN']

PLUGINS = [
        'plugins',
        ]
