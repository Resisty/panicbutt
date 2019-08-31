#!/usr/bin/python
""" Jeff plugin module for panicbutt
"""
# =======================================
#
#  File Name : jeff.py
#
#  Purpose : Keep track of Jeff's level of existential crisis.
#
#  Creation Date : 01-05-2015
#
#  Last Modified : Wed 12 Apr 2017 03:21:57 PM CDT
#
#  Created By : Brian Auron
#
# ========================================
import datetime
import re
import os
import peewee
import yaml
from playhouse.postgres_ext import PostgresqlExtDatabase

import slackbot.bot

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
YAML_LOC = os.path.join(BASE_DIR, '../config.yml')
with open(YAML_LOC, 'r') as fptr:
    CFG = yaml.load(fptr.read())
DBUSER = CFG['dbuser']
DBPASS = CFG['dbpass']
DB = CFG['db']
PSQL_DB = PostgresqlExtDatabase(DB, user=DBUSER, password=DBPASS)

class JeffCrisis(peewee.Model):
    """ DB model abstracting Jeff's crises
    """
    nick = peewee.CharField()
    datetime = peewee.DateTimeField()
    level = peewee.CharField()

    # pylint: disable=too-few-public-methods
    class Meta:
        """ Metaclass, set db connection
        """
        database = PSQL_DB

class Level(peewee.Model):
    """ DB Model tracking Jeff's crisis level
    """
    name = peewee.TextField(unique=True)
    text = peewee.TextField(default='black')
    font = peewee.TextField(default='Lucida Console')
    bg = peewee.TextField(default='critical.gif')

    # pylint: disable=too-few-public-methods
    class Meta:
        """ Metaclass, set db connection
        """
        database = PSQL_DB

def create_crisis():
    """ Convenience function, create the crisis table
    """
    PSQL_DB.connect()
    PSQL_DB.create_tables([JeffCrisis, Level])

def drop_crisis():
    """ Convenience function, drop the crisis table
        Suggest only using it for development purposes
    """
    PSQL_DB.connect()
    PSQL_DB.drop_tables([JeffCrisis, Level])

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
    """ Get current crisis level from DB
    """
    recent = JeffCrisis.select().order_by(JeffCrisis.id.desc()).get()
    return recent.level.lower()

def set_crisis_level(nick, level):
    """ Set current crisis level in DB

        :param nick: Slack nick; user whose crisis level we're setting
        :param level: crisis level being set
    """
    level = level.lower()
    link = "http://brianauron.info/jeff-existential-crisis-level/"
    if get_current_level() != level:
        PSQL_DB.connect()
        JeffCrisis.create(nick=nick, datetime=datetime.datetime.now(), level=level)
        text = "Jeff's existential crisis level has been set to " + level
    else:
        text = "Jeff's existential crisis level is already {0}, ya jerk!".format(level)
    text += "\n{0}".format(link)
    return text

def til_sane():
    """ Super specific function calculating the time until Jeff becomes sane.
        Probably best if we don't explain further.
    """
    grad = datetime.date(2016, 5, 31)
    diff = grad - datetime.date.today()
    data = f'Assuming he sticks to the plan, Jeff becomes sane in {str(diff.days)} days.'
    return data

JEFFSTRING = r'''([\s\w\']+)\s
                 Jeff
                 ($|\sbecomes\ssane|\sgraduates)'''
JEFF = re.compile(JEFFSTRING, re.IGNORECASE | re.VERBOSE)
@slackbot.bot.listen_to(JEFF)
def jeff_info(message, *groups):
    """ Listen for queries about Jeff and respond

        :param message: Raw message query
        :param groups: re.search() groups
    """
    verb = groups[0]
    verbs = [i.name for i in Level.select()]
    if verb in verbs:
        # pylint: disable=protected-access
        user = message._client.users[message._get_user_id()]['name']
        message.reply(set_crisis_level(user, verb))
    elif verb in ['list', 'enumerate', 'print']:
        message.reply(', '.join(JEFF_CRISIS_LEVELS.keys()))
    elif verb in ['link', 'url']:
        message.reply('http://brianauron.info/jeff-existential-crisis-level/')
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
