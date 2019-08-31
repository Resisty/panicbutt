#!/usr/bin/python
""" Run the slack bot
"""

import os
import sys
sys.path.insert(0, f'{os.getcwd()}')
# pylint: disable=wrong-import-position
import slackbot.bot

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(BASE_DIR, 'config.yml')

def main():
    """ Main execution function
    """
    bot = slackbot.bot.Bot()
    bot.run()

if __name__ == '__main__':
    main()
