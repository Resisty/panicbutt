#!/usr/bin/python
# =======================================
#
#  File Name : reddit.py
#
#  Purpose : take r/subreddit and make it a clickable link
#
#  Creation Date : 12-02-2018
#
#  Last Modified : Mon 12 February 2018 10:31:27 AM EST
#
#  Created By : Edward Olsen
#
# ========================================

import slackbot.bot
import re

REDDIT_REGEX = "((\/r\/)|(r\/))(\w+)"
REDDIT = re.compile(REDDIT_REGEX, re.IGNORECASE)
@slackbot.bot.listen_to(REDDIT)
def reddit(message, *groups):

	matches = re.search(REDDIT_REGEX, message_text)         
	subreddit = matches.group(4) 
	msg ="http://reddit.com/r/{}".format(subreddit)
	message.reply(msg)
