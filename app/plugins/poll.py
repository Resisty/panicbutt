#!/usr/bin/python
""" Module for creating and tracking polls
"""

import os
import functools
import peewee
import playhouse.postgres_ext as pe
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(BASE_DIR, '../config.yml')
with open(CONFIG, 'r') as yml:
    CFG = yaml.load(yml.read())
DBUSER = CFG['dbuser']
DBPASS = CFG['dbpass']
DB = CFG['db']
PSQL_DB = pe.PostgresqlExtDatabase(DB, user=DBUSER, password=DBPASS)

def connect(func):
    """ Connection decorator
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
    """ DB model for a poll
    """
    title = peewee.TextField()
    opened = peewee.DateTimeField()
    close = peewee.DateTimeField()
    closed = peewee.BooleanField(default=False)

class Option(peewee.Model):
    """ DB model for a poll option
    """
    name = peewee.TextField()
    poll = peewee.ForeignKeyField(Poll, related_name='related_poll')

    # pylint: disable=too-few-public-methods
    class Meta:
        """ Metaclass; set up db connection
        """
        database = PSQL_DB

class User(peewee.Model):
    """ DB model for a user
    """
    name = peewee.CharField(unique=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """ Metaclass; set up db connection
        """
        database = PSQL_DB

class User2Option(peewee.Model):
    """ DB model for pairing users and options
    """
    option = peewee.ForeignKeyField(Option)
    user = peewee.ForeignKeyField(User)
    vote = peewee.IntegerField(constraints=[peewee.Check('vote = 1')])
    # pylint: disable=too-few-public-methods
    class Meta:
        """ Metaclass; set up db connection
            Also set up an index on options and users
        """
        indexes = (
            (('option', 'user'), True),
        )
        database = PSQL_DB

def create_ratings():
    """ Convenience function; create poll table
    """
    PSQL_DB.connect()
    PSQL_DB.create_tables([Poll, Option, User, User2Option])

def drop_ratings():
    """ Convenience function; drop poll table
    """
    PSQL_DB.connect()
    PSQL_DB.drop_tables([Poll, Option, User, User2Option])

@connect
def poll_results(poll_id):  # pylint: disable=unused-argument
    """ I guess I never finished this
    """
