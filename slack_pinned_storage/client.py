#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dateutil.parser
import requests
import json
import os
import re

from datetime import date, datetime

SLACK_API = 'https://slack.com/api/'
SLACK_METHODS = {
    'getPinnedMessages': 'pins.list', 
    'addPin': 'pins.add',
    'postMessage': 'chat.postMessage',
    'updateMessage': 'chat.update',
    'getChannels': 'channels.list',
}

class SlackPinnedStorage(object):
    """
    Client
    """
    def __init__(self, token, storageKey, channel='#general', username='slack_pinned_storage'):
        self.token = token
        self.storageKey = storageKey
        self.channel = self.fetchChannelId(channel) if channel.startswith('#') else channel
        self.username = username

        fetched = self.fetchRemoteStorage()
        self.data = fetched.get('data')
        self.ts = fetched.get('ts')

    def fetchChannelId(self, channelName):
        response = requests.get(SLACK_API + SLACK_METHODS['getChannels'], params={
            'token': self.token,
        }).json()

        channelName = re.sub(r'^#', '', channelName)

        if response.get('ok'):
            for channel in response.get('channels'):
                if channel.get('name') == channelName:
                    return channel

    def fetchRemoteStorage(self):
        response = requests.get(SLACK_API + SLACK_METHODS['getPinnedMessages'], params={
            'token': self.token,
            'channel': self.channel,
        }).json()

        if response.get('ok'):
            items = response.get('items')

            for item in items:
                if item.get('type') == 'message':
                    storage = item.get('message', {}).get('text', '').startswith(self.storageKey)

                    return {
                        'data': self.parseDataText(storage.get('text')),
                        'ts': storage.get('ts'),
                    }

    def generateDataText(self, data):
        text = self.storageKey + json.dumps(data, default=json_serializer)
        return text

    def parseDataText(self, storageString=''):
        if storageString == '':
            return '' 
        jsonString = re.sub(self.storageKey, '', storageString, 1)
        return json.loads(jsonString, object_hook=json_parser)

    def createRemoteStorage(self, message):
        response = requests.post(SLACK_API + SLACK_METHODS['postMessage'], data={
            'token': self.token,
            'channel': self.channel,
            'text': self.generateDataText(message),
            'username': self.username,
        }).json()

        if response.get('ok'):
            self.data = self.parseDataText(response.get('message', {}).get('text'))
            self.ts = response.get('ts')

            requests.post(SLACK_API + SLACK_METHODS['addPin'], data={
                'token': self.token,
                'channel': self.channel,
                'timestamp': self.ts
            })

        return self.data

    def updateRemoteStorage(self, message):
        response = requests.post(SLACK_API + SLACK_METHODS['updateMessage'], data={
            'token': self.token,
            'channel': self.channel,
            'text': self.generateDataText(message),
            'ts': self.ts,
            'username': self.username,
        }).json()

        if response.get('ok'):
            self.data = self.parseDataText(response.get('text'))
            self.ts = response.get('ts')

        return self.data

    def set(self, value):
        if self.data and self.ts:
            self.updateRemoteStorage(value)
        else:
            self.createRemoteStorage(value)
        return self

    def get(self):
        return self.data

def json_serializer(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    raise TypeError ('Type %s not serializable' % type(value))

def json_parser(data):
    for key, value in data.items():
        if isinstance(value, str):
            try:
                data[key] = dateutil.parser.parse(value)
            except:
                pass
    return data
