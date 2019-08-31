#!/usr/bin/python
# =======================================
#
#  File Name : slackbot_settings.py
#
#  Purpose :
#
#  Creation Date : 18-03-2016
#
#  Last Modified : Tue 12 Apr 2016 04:43:10 PM CDT
#
#  Created By : Brian Auron
#
# ========================================

import yaml
from runbot import CONFIG
with open(CONFIG, 'r') as yml:
    config = yaml.load(yml.read())

default_reply = "I'm sorry, Dave, I'm afraid I can't do that."

API_TOKEN = config['API_TOKEN']

PLUGINS = [
        'plugins',
        ]
