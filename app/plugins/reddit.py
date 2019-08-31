#!/usr/bin/python
# =======================================
#
#  File Name : reddit.py
#
#  Purpose : take r/subreddit and make it a clickable link
#
#  Creation Date : 12-02-2018
#
#  Last Modified : Fri 16 Feb 2018 03:36:13 PM CST
#
#  Created By : Edward Olsen
#
# ========================================

import slackbot.bot
import re

REDDIT_REGEX = "\s*((\/r\/)|(r\/))(\w+)\s*"
REDDIT = re.compile(REDDIT_REGEX, re.IGNORECASE)
@slackbot.bot.listen_to(REDDIT)
def reddit(message, *groups):
	subreddit = groups[3]
	msg ="http://reddit.com/r/{}".format(subreddit)
	message.reply(msg)
