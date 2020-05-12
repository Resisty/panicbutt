#!/usr/bin/env python

import slackbot.bot
import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(BASE_DIR, 'config.yml')

def main():
    logging.basicConfig()
    LOGGER = logging.getLogger('slackbot')
    bot = slackbot.bot.Bot()
    bot.run()

if __name__ == '__main__':
    main()
