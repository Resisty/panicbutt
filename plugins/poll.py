#!/usr/bin/env python
""" Unfinished module for conducting polls
"""

import os
import functools
import peewee
import playhouse.postgres_ext as pe
import yaml

# pylint: disable=too-few-public-methods

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(BASE_DIR, '../config.yml')
with open(CONFIG, 'r') as yml:
    CFG = yaml.load(yml.read(), Loader=yaml.FullLoader)
DBUSER = CFG['dbuser']
DBPASS = CFG['dbpass']
DB = CFG['db']
PSQL_DB = pe.PostgresqlExtDatabase(DB, user=DBUSER, password=DBPASS)

def connect(func):
    """ DB connection decorator
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            PSQL_DB.connect()
            return func(*args, **kwargs)
        finally:
            PSQL_DB.close()
    return wrapper

class Poll(peewee.Model):
    """ DB model for polls
    """
    title = peewee.TextField()
    opened = peewee.DateTimeField()
    close = peewee.DateTimeField()
    closed = peewee.BooleanField(default=False)

class Option(peewee.Model):
    """ DB model for poll options
    """
    name = peewee.TextField()
    poll = peewee.ForeignKeyField(Poll, related_name='related_poll')

    class Meta:
        """ metaclass holding connection
        """
        database = PSQL_DB

class User(peewee.Model):
    """ DB model for poll responders
    """
    name = peewee.CharField(unique=True)

    class Meta:
        """ metaclass holding connection
        """
        database = PSQL_DB

class User2Option(peewee.Model):
    """ Multi-to-multi join on users and options
    """
    option = peewee.ForeignKeyField(Option)
    user = peewee.ForeignKeyField(User)
    vote = peewee.IntegerField(constraints=[peewee.Check('vote = 1')])
    class Meta:
        """ Metaclass holding db connection and index on options<->users
        """
        indexes = (
            (('option', 'user'), True),
        )
        database = PSQL_DB

def create_ratings():
    """ Create the tables necessary for polls
    """
    PSQL_DB.connect()
    PSQL_DB.create_tables([Poll, Option, User, User2Option])

def drop_ratings():
    """ Drop tables necessary for polls
    """
    PSQL_DB.connect()
    PSQL_DB.drop_tables([Poll, Option, User, User2Option])

@connect
def poll_results(poll_id):  # pylint: disable=unused-argument
    """ Not implemented
    """
    # TODO: get poll results by id or something  # pylint: disable=fixme
