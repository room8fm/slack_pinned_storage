#!/usr/bin/env python
# -*- coding: utf-8 -*-

import umsgpack
import requests
import json
import os
import re

SLACK_API = 'https://slack.com/api/'
SLACK_METHODS = {
    'getPinnedMessages': 'pins.list', 
    'addPin': 'pins.add',
    'postMessage': 'chat.postMessage',
    'getChannels': 'channels.list',
}

class Client(object):
    """
    Client
    """
    def __init__(self, token, storageKey, channel='#general', username='slack_pinned_storage'):
        self.token = token
        self.storageKey = storageKey
        self.channel = self.fetchChannelId(channel) if channel.startswith('#') else channel
        self.username = username
        self.storage = self.fetchRemoteStorage()

    def fetchChannelId(self, channelName):
        response = requests.get(SLACK_API + SLACK_METHODS['getChannels'], params={
            'token': self.token,
        }).json()

        if not response['ok']:
            return None

        name = re.sub(r'^#', '', channelName)
        return [channel['id'] for channel in response['channels'] if channel['name'] == name]

    def fetchRemoteStorage(self):
        response = requests.get(SLACK_API + SLACK_METHODS['getPinnedMessages'], params={
            'token': self.token,
            'channel': self.channel,
        }).json()

        if response['ok']:
            storageString = [item['message'] for item in response['items'] if item['message'].startswith(self.storageKey)]

            if storageString:
                return re.sub(self.storageKey, '', storageString, 1)

        return None

    def set(self, value):
        return value;

    def get(self):
        return value
