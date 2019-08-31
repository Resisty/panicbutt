#!/usr/bin/python
""" Run the slack bot
"""

import os
import sys
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
