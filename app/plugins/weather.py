# -*- coding: utf-8 -*-
#!/usr/bin/python
""" Module for using pyowm in a slackbot
"""

import os
import re
import pyowm
import yaml
import slackbot.bot

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(BASE_DIR, '../config.yml')
with open(CONFIG, 'r') as yml:
    CFG = yaml.load(yml.read())
APIKEY = CFG['owm']['key']
NUM_WEATHERS = 3

class WeatherBot:
    """ Abstraction around pyowm
    """
    def __init__(self, apikey=APIKEY):
        self._owm = pyowm.OWM(apikey)
        self._num = NUM_WEATHERS
    def weather_at(self, location, num=None):
        """ Get weather at a location
        """
        if num:
            self._num = num
        forecaster = (self
                      ._owm
                      .three_hours_forecast(location))
        forecast = forecaster.get_forecast()
        for weather in forecast.get_weathers()[:self._num]:
            yield weather
    @property
    def num(self):
        """ I don't remember what this is
        """
        return self._num

WEATHERSTRING = r'''weather\s(.*)'''
WEATHER = re.compile(WEATHERSTRING, re.IGNORECASE|re.VERBOSE)
@slackbot.bot.respond_to(WEATHER)
def weather_where(message, *groups):
    """ Respond to requests for weather at a place
    """
    location = groups[0]
    wbot = WeatherBot()
    msg = u'Next %s 3-hour weathers for %s\n' % (wbot.num, location)
    for weather in wbot.weather_at(location):
        msg += f'{weather.get_detailed_status()}({weather.get_temperature("fahrenheit")["temp"]}ºF)\n'
    message.reply(msg)
    #print 'Got a message %s with groups "%s"' % (message.body, groups)
