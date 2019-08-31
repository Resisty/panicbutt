#!/usr/bin/env python
""" Module for using the imgur api in a slack bot
"""
import math
import random
import re
import requests
import slackbot.bot

IMGUR_ID = '7fd4f416717f07d'
IMGUR_URI = 'https://api.imgur.com/3/gallery/search'

# pylint: disable=too-few-public-methods
class QueryParam:
    """ Abstraction for constructing query parameters for imgur requests
    """
    @classmethod
    def from_type(cls, query_type):
        """ Return a query parameter from a type
        """
        return {'image': {'q_type': 'png'},
                'animate': {'q_type': 'anigif'}}[query_type]

@slackbot.bot.listen_to(re.compile('^(image|animate) (.*)$', re.I))
def imgur(message, *groups):
    """ Listen for and reply to imgur messages
    """
    q_type = QueryParam.from_type(groups[0])
    query = groups[1]
    params = {'q': query}
    params.update(q_type)
    headers = {'Authorization': 'Client-ID %s' % IMGUR_ID}
    response = requests.get(IMGUR_URI, params=params, headers=headers)
    if not response.ok:
        message.reply('herp derp problems connecting to imgur API')
        return
    data = response.json()['data']
    if not data:
        message.reply('durrr no results found durrr')
        return
    index = int(random.expovariate(math.sqrt(2)/2))
    if index > len(data):
        index = 0
    message.reply(data[index]['link'])
