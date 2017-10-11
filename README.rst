=====================
Slack Pinned Storage
=====================

Requirements
================
A Slack app token with following permission scopes.

- chat:write:bot(required)
- pins:read(required)
- pins:write(required)
- channels:read(optional)

``channels:read`` is not required when channelId is given.

`SlackApps <https://api.slack.com/apps>`_

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
  >>> {'hello': 'python', 'fun': True}


After setting a value, post a json-stringified data as a message in the channel.
``IDENTIFIER_STRING{"hello": "python", "fun": true}``
