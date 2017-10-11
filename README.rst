=====================
Slack Pinned Storage
=====================

Requirements
================
https://api.slack.com/apps

Basic Usage
================

Setting and getting a value
******************************

.. code-block:: python

  from slack_pinned_storage import SlackPinnedStorage

  token = 'YOUR_SLACK_APP_TOKEN'
  storageIdentifier = 'IDENTIFIER_STRING'
  channel = '#channelName' or 'IDXXXXX'

  sps = SlackPinnedStorage(token, storageIdentifier, channel)

  sps.set({'hello': 'python', 'fun': True})
  sps.get()

After setting a value, post a json-stringified data as a message in the channel.
``IDENTIFIER_STRING{"hello": "python", "fun": true}``
