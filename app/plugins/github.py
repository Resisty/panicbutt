#!/usr/bin/python
# =======================================
#
#  File Name : github.py
#
#  Purpose :
#
#  Creation Date : 27-03-2016
#
#  Last Modified : Tue 29 Mar 2016 05:28:59 PM CDT
#
#  Created By : Brian Auron
#
# ========================================

import requests
import yaml
import json
import os
import re
import slackbot.bot

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(BASE_DIR, '../config.yml')
with open(CONFIG, 'r') as yml:
    cfg = yaml.load(yml.read())

URL = cfg['github']['url']
OWNER = cfg['github']['owner']
REPO = cfg['github']['repo']
TOKEN = cfg['github']['token']
HEADERS = {'Content-Type': 'application/json',
           'Authorization': 'token %s' % TOKEN}

class Issue(object):
    def __init__(self):
        self.uri = URL+'/repos/%s/%s/issues' % (OWNER, REPO)
    def list(self, params={}):
        req = requests.get(self.uri, headers=HEADERS, params=params)
        return json.loads(req.text)
    def create(self, title, body):
        data = {'title': title, 'body': body}
        req = requests.post(self.uri, headers=HEADERS, data=json.dumps(data))
        return json.loads(req.text)


LISTISSUESTRING = r'''github\slist\sissues?
                      ($|\sopen|\sclosed)?
                      ($|\sexpanded)'''
LISTISSUES = re.compile(LISTISSUESTRING, re.IGNORECASE|re.VERBOSE)
@slackbot.bot.respond_to(LISTISSUES)
def list_issues(message, *groups):
    param = groups[0]
    expanded = groups[1]
    params = {}
    if param:
        params['state'] = param
    resp = Issue().list(params=params)
    if len(resp) == 0:
        message.reply('0 issues found.')
        return
    if expanded:
        for i in resp:
            (message.reply('Issue: %s\nTitle: %s\nDescription: %s' %
                (i['html_url'], i['title'], i['body'])))
    else:
        [message.reply(i['html_url']) for i in resp]
    #print 'Got a message %s with groups "%s"' % (message.body, groups)

CREATEISSUESTRING = r'''github\screate\sissue\s
                        ((title\s)?(".*"))\s
                        ((body\s)?(".*"))$'''
CREATEISSUE = re.compile(CREATEISSUESTRING, re.IGNORECASE|re.VERBOSE)
@slackbot.bot.respond_to(CREATEISSUE)
def create_issue(message, *groups):
    title = groups[2].strip('"')
    body = groups[5].strip('"')
    resp = Issue().create(title, body)
    message.reply(resp['html_url'])
    #print 'Got a message %s with groups "%s"' % (message.body, groups)
