#!/usr/bin/env python

import slackbot.bot
import logging
import sys
import os

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(BASE_DIR, 'config.yml')

def main():
    logging.basicConfig()
    bot = slackbot.bot.Bot()
    bot.run()

if __name__ == '__main__':
    main()
