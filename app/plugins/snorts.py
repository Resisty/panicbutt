#!/usr/bin/python
""" Module for counting snorts... and other things
"""

import functools
import datetime
import operator
import re
import os
import slackbot.bot
import peewee
import yaml
from playhouse.postgres_ext import PostgresqlExtDatabase
import app.plugins.fakenumbers

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(BASE_DIR, '../config.yml')
with open(CONFIG, 'r') as fptr:
    CFG = yaml.load(fptr.read(), Loader=yaml.FullLoader)
DBUSER = CFG['dbuser']
DBPASS = CFG['dbpass']
DB = CFG['db']
PSQL_DB = PostgresqlExtDatabase(DB, user=DBUSER, password=DBPASS)

def user(msg):
    """ Get user name from message
    """
    # pylint: disable=protected-access
    return msg._client.users[msg._get_user_id()]['name']

def users(msg):
    """ Get list of users from message
    """
    # pylint: disable=protected-access
    return [j['name'] for i, j in msg._client.users.items()]

class BaseModel(peewee.Model):
    """ DB model base class
    """
    # pylint: disable=too-few-public-methods
    class Meta:
        """ Metaclass; set up db connection
        """
        database = PSQL_DB


class Snorts(BaseModel):
    """ DB model for snorts
    """
    nick = peewee.CharField()
    day = peewee.DateField()
    count = peewee.IntegerField(default=0)


class Counts(BaseModel):
    """ DB model for counting things
    """
    key = peewee.CharField(unique=True)
    count = peewee.IntegerField(default=0)
    day = peewee.DateField(null=True)


def connect(func):
    """ DB connection decorator
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """ Wrap the connection
        """
        try:
            PSQL_DB.connect()
            return func(*args, **kwargs)
        finally:
            PSQL_DB.close()
    return wrapper

@connect
def create_tables():
    """ Convenience function; create the tables
    """
    PSQL_DB.create_tables([Snorts, Counts])

@connect
def drop_tables():
    """ Convenience function; drop the tables
    """
    PSQL_DB.connect()
    PSQL_DB.drop_tables([Snorts, Counts])

def do_snort(nick):
    """ Do (record) a snort
    """
    day = datetime.date.today()
    try:
        row = Snorts.select().where((Snorts.nick == nick) &
                                    (Snorts.day == day)).get()
    except peewee.DoesNotExist:
        row = Snorts.create(nick=nick, day=day)
    Snorts.update(count=Snorts.count + 1).where(Snorts.id == row.id).execute()
    row = Snorts.select().where(Snorts.id == row.id).get()
    return f'{row.nick} has snorted {row.count} snorts today.'

SNORTSTRING = r'''snort\s
                  ([\w-]+)'''
SNORT = re.compile(SNORTSTRING, re.IGNORECASE|re.VERBOSE)
@slackbot.bot.respond_to(SNORT)
def snort_me(message, *groups):
    """ Respond to a request for a snort
    """
    who = groups[0]
    if who == 'me':
        who = user(message)
    nicks = users(message)
    if who not in nicks:
        message.reply(f'Cannot snort {who} a snort, nick not in channel.')
    else:
        message.reply(do_snort(who))
    data = {}
    data['reply'] = 'public'
    return data

SHOWSNORTSTRING = r'''show\ssnorts'''
SHOWSNORT = re.compile(SHOWSNORTSTRING, re.IGNORECASE|re.VERBOSE)
@slackbot.bot.respond_to(SHOWSNORT)
def show_snorts(message):
    """ Respond to a request for list of snorts
    """
    day = datetime.date.today()
    rows = Snorts.select().where(Snorts.day == day)
    results = []
    for row in rows:
        results.append(f'{row.nick} has snorted {row.count} snorts today.')
    if results == []:
        results.append('Nobody has snorted a snort today!')
    message.reply('\n'.join(results))

COUNTINGSTRING = r'''^([\w\.-]+)
                     (\+\+|--)$'''
COUNTING = re.compile(COUNTINGSTRING, re.IGNORECASE|re.VERBOSE)
@slackbot.bot.listen_to(COUNTING)
def count_update(message, *groups):
    """ Adjust the count of something
    """
    key, delta = groups
    key = key.lower()
    delta = {'++': 1, '--': -1}[delta]
    try:
        counter = app.plugins.fakenumbers.NumberString.from_str(key)
        counter += delta
        message.reply(counter.str)
        return
    except app.plugins.fakenumbers.NoNumberError:
        pass
    with PSQL_DB.atomic():
        try:
            count = Counts.create(key=key, count=0)
        except peewee.IntegrityError:
            PSQL_DB.connect() # not entirely sure why this is necessary but it is
            count = Counts.get(Counts.key == key)
        count.count += delta
        count.save()
    message.reply(f'{key} is now {count.count}')

ARITHMETICSTRING = r'''^([\w\.-]+)\s
                     ([+\-\*/])=\s
                     (-?\d+)$'''
ARITHMETIC = re.compile(ARITHMETICSTRING, re.IGNORECASE|re.VERBOSE)
@slackbot.bot.listen_to(ARITHMETIC)
def arithmetic_update(message, *groups):
    '''Adjust a count arithmetically
Examples: a += 3
          counting -= 2
          stuff *= 0
          things /= 1'''
    key, oper, amount = groups
    key = key.lower()
    oper = {'+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.floordiv}[oper]
    with PSQL_DB.atomic():
        try:
            count = Counts.create(key=key, count=0)
        except peewee.IntegrityError:
            PSQL_DB.connect() # not entirely sure why this is necessary but it is
            count = Counts.get(Counts.key == key)
        try:
            count.count = oper(count.count, int(amount))
        except ZeroDivisionError:
            message.reply('You can\'t divide by zero, stupid!')
            return
        count.save()
    message.reply('{key} is now {count.count}')

DELCOUNTSTRING = r'''delete\s
                     (\w+)$'''
DELCOUNT = re.compile(DELCOUNTSTRING, re.IGNORECASE|re.VERBOSE)
@slackbot.bot.respond_to(DELCOUNT)
def count_delete(message, *groups):
    """ Delete a count of something
    """
    key = groups[0]
    key = key.lower()
    try:
        count = Counts.select().where(Counts.key == key, Counts.count == 0).get()
        count.delete_instance()
        msg = f'{key} has been deleted.'
    except peewee.DoesNotExist:
        msg = f'{key} does not exist in the Counts table or it does not have a count of 0!'
    message.reply(msg)

GETCOUNTSTRING = r'''print\s
                     (\w+)$'''
GETCOUNT = re.compile(GETCOUNTSTRING, re.IGNORECASE|re.VERBOSE)
@slackbot.bot.respond_to(GETCOUNT)
def count_get(message, *groups):
    """ Get a count of something
    """
    key = groups[0]
    key = key.lower()
    try:
        message.reply(str(Counts.get(Counts.key == key).count))
    except peewee.DoesNotExist:
        message.reply('None')

GETCOUNTS_STRING = r'''list\scounts'''
GETCOUNTS = re.compile(GETCOUNTS_STRING, re.IGNORECASE|re.VERBOSE)
@slackbot.bot.respond_to(GETCOUNTS)
def count_list(message):
    """ Respond to a request to list all counts of things
    """
    try:
        message.reply(', '.join([i.key for i in Counts.select()]))
    except peewee.DoesNotExist:
        message.reply('Could not find keys for counts!')

JEFFWROTESTRING = r'''.*'''
JEFFWROTE = re.compile(JEFFWROTESTRING, re.IGNORECASE|re.VERBOSE)
@slackbot.bot.listen_to(JEFFWROTE)
def annoy_jeff(message):
    """ Annoy the hell out of Jeff
    """
    # pylint: disable=protected-access
    if message._get_user_id() != CFG['HUGHLOLRUS_ID']:
        return
    PSQL_DB.connect()
    try:
        previous = Counts.get(Counts.key == 'DaysWithoutResume').day
    # pylint: disable=broad-except
    except Exception:
        return
    today = datetime.datetime.now().date()
    if today > previous:
        query = (Counts
                 .update(day=today)
                 .where(Counts.key == 'DaysWithoutResume'))
        query.execute()
        msg = 'UPDATE YOUR RESUME, SEND IT TO DK, AND GET SOME JOB/LIFE BALANCE/SATISFACTION FFS'
        message.reply(msg)
