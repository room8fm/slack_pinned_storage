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
    'updateMessage': 'chat.update',
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

        fetched = self.fetchRemoteStorage()
        self.data = fetched['data'] if fetched else None
        self.ts = fetched['ts'] if fetched else None

    def fetchChannelId(self, channelName):
        response = requests.get(SLACK_API + SLACK_METHODS['getChannels'], params={
            'token': self.token,
        }).json()

        if not response['ok']:
            return None

        name = re.sub(r'^#', '', channelName)
        channel = [channel['id'] for channel in response['channels'] if channel['name'] == name]
        return channel[0] if channel else None

    def fetchRemoteStorage(self):
        response = requests.get(SLACK_API + SLACK_METHODS['getPinnedMessages'], params={
            'token': self.token,
            'channel': self.channel,
        }).json()

        if response['ok']:
            items = response['items']
            storageItem = [item['message'] for item in items if item['type'] == 'message' and item['message']['text'].startswith(self.storageKey)]

            if storageItem:
                return {
                    'data': self.parseDataText(storageItem[0]['text']),
                    'ts': storageItem[0]['ts']
                }
        return None

    def generateDataText(self, data):
        text = self.storageKey + json.dumps(data)
        return text

    def parseDataText(self, storageString):
        jsonString = re.sub(self.storageKey, '', storageString, 1)
        return json.loads(jsonString)

    def createRemoteStorage(self, message):
        response = requests.post(SLACK_API + SLACK_METHODS['postMessage'], data={
            'token': self.token,
            'channel': self.channel,
            'text': self.generateDataText(message),
            'username': self.username,
        }).json()

        if response['ok']:
            self.data = self.parseDataText(response['message']['text'])
            self.ts = response['ts']

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

        if response['ok']:
            self.data = self.parseDataText(response['text'])
            self.ts = response['ts']

        return self.data

    def set(self, value):
        if self.data and self.ts:
            self.updateRemoteStorage(value)
        else:
            self.createRemoteStorage(value)
        return self

    def get(self):
        return self.data
