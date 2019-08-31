#!/usr/bin/python
""" Module for constructing reddit links from messages
"""

import re
import slackbot.bot

REDDIT_REGEX = r"\s*((\/r\/)|(r\/))(\w+)\s*"
REDDIT = re.compile(REDDIT_REGEX, re.IGNORECASE)
@slackbot.bot.listen_to(REDDIT)
def reddit(message, *groups):
    """ Listen to messages that might container reddit references
    """
    subreddit = groups[3]
    msg = "http://reddit.com/r/{}".format(subreddit)
    message.reply(msg)
