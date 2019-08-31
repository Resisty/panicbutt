#!/usr/bin/python
""" Module for using the urbandictionary api in a slack bot
"""

import re
import traceback
import requests
import slackbot.bot

URBANSTRING = r'''urban\s([\w\s-]+)($|\s#\d+)'''
URBAN = re.compile(URBANSTRING, re.IGNORECASE)
@slackbot.bot.respond_to(URBAN)
def urban(message, *groups):
    """ Respond to urbandictionary requests
    """
    try:
        what = groups[0]
        what = what.replace(' ', '%20')
        which = groups[1]
        if which:
            which = int(groups[1].strip().split('#')[1]) - 1
        else:
            which = 0
        url = 'http://api.urbandictionary.com/v0/define?term={0}'
        url = url.format(what)
        results = requests.get(url)
        jdata = results.json()
        if 'list' not in jdata or not jdata['list']:
            msg = 'That\'s a stupid search!'
        else:
            try:
                msg = jdata['list'][which]['definition']
            except IndexError:
                msg = 'No such definition number!'
        message.reply(msg)
    # pylint: disable=broad-except
    except Exception:
        print(traceback.format_exc())
