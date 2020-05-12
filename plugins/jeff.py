#!/usr/bin/env python
""" Module for fucking with Jeff
"""
import datetime
import re
import json

import boto3
import slackbot.bot

BUCKET = 'brianauron.info'
KEY = 'jeff-existential-crisis-level/jeff.json'
JEFF_CRISIS_LEVELS = {'critical' : {'text' : 'black',
                                    'font' : 'Lucida Console',
                                    'bg' : "critical.gif"},
                      'too damn high' : {'text' : 'red',
                                         'font' : 'Lucida Console',
                                         'bg' : "toodamnhigh.gif"},
                      'cat' : {'text' : 'white',
                               'font' : 'Arial',
                               'bg' : "expressive_cat.png"},
                      'can\'t even' : {'text' : 'purple',
                                       'font' : 'Impact',
                                       'bg' : "canteven.gif"},
                      'pants meat' : {'text' : 'pink',
                                      'font' : 'Times New Roman',
                                      'bg' : "pantsmeat.gif"},
                      'under control' : {'text' : 'yellow',
                                         'font' : 'Cursive',
                                         'bg' : "undercontrol.gif"},
                      'awol' : {'text' : 'orange',
                                'font' : 'Impact',
                                'bg' : "awol.gif"},
                      'linuxpocalypse' : {'text' : 'green',
                                          'font' : 'Impact',
                                          'bg' : "tux.gif"}}

def get_current_level():
    """ Obtain Jeff's current existential crisis level from the '''database'''
    """
    s3cli = boto3.Session().client('s3')
    data = s3cli.get_object(Bucket=BUCKET, Key=KEY)['Body'].read()
    return json.loads(data)['level'].lower()

def set_crisis_level(nick, level):  # pylint: disable=unused-argument
    """ Set Jeff's current existential crisis level for user with nickname 'nick'
    """
    level = level.lower()
    link = "http://brianauron.info.s3-website.us-west-2.amazonaws.com/jeff-existential-crisis-level/"
    text = ''
    try:
        if get_current_level() != level:
            data = JEFF_CRISIS_LEVELS[level]
            data['level'] = level
            s3cli = boto3.Session().client('s3')
            s3cli.put_object(Bucket=BUCKET, Key=KEY, Body=json.dumps(data).encode('utf-8'))
        else:
            text = f"Jeff's existential crisis level is already {level}, ya jerk!"
        text += f"\n{link}"
    except KeyError:
        text = f"'{level}' is not a supported existential crisis level for Jeff, ya jerk!"
    return text

def til_sane():
    """ Calculate how long it'll be until Jeff is sane... maybe
    """
    grad = datetime.date(2016, 5, 31)
    diff = grad - datetime.date.today()
    data = 'Assuming he sticks to the plan, Jeff becomes sane in {0} days.'.format(str(diff.days))
    return data

JEFFSTRING = r'''([\s\w\']+)\s
                 Jeff
                 ($|\sbecomes\ssane|\sgraduates)'''
JEFF = re.compile(JEFFSTRING, re.IGNORECASE | re.VERBOSE)
@slackbot.bot.listen_to(JEFF)
def jeff_info(message, *groups):
    """ Enumerate bot's abilities for fucking with Jeff
    """
    verb = groups[0]
    verbs = JEFF_CRISIS_LEVELS.keys()
    if verb in verbs:
        user = message._client.users[message._get_user_id()]['name']  # pylint: disable=protected-access
        message.reply(set_crisis_level(user, verb))
    elif verb in ['list', 'enumerate', 'print']:
        message.reply(', '.join(JEFF_CRISIS_LEVELS.keys()))
    elif verb in ['link', 'url']:
        message.reply('http://brianauron.info.s3-website.us-west-2.amazonaws.com/jeff-existential-crisis-level/')
    elif verb in ['what is']:
        message.reply(get_current_level())
    elif verb in ['how long until', 'when will']:
        try:
            sanity = groups[1]
            if not sanity:
                raise ValueError('Need a state of being for Jeff!')
        except (IndexError, ValueError):
            message.reply(f'{verb.capitalize()} Jeff what?')
        else:
            message.reply(til_sane())
    else:
        message.reply(f'{verb.capitalize()} Jeff what?')
