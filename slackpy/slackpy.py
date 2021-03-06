#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Takahiro Ikeuchi'

import os
import requests
import json
from argparse import ArgumentParser


class SlackLogger:
    def __init__(self, webhook_url, channel, username='Logger'):

        self.base_uri = '{0}'.format(webhook_url)
        self.channel = channel
        self.username = username

    def __send_notification(self, message, title='Slack Notification', color='good'):
        """Send a message to a channel.
        Args:
            title: The message title.
            message: The message body.
            color: Can either be one of 'good', 'warning', 'danger', or any hex color code

        Returns:
            api_response:

        Raises:
            TODO:
        """
        __fields = {
            "title": title,
            "text": message,
            "color": color,
            "fallback": title,
        }

        __attachments = {
            "fields": __fields
        }

        payload = {
            "channel": self.channel,
            "username": self.username,
            "attachments": __attachments
        }

        response = requests.post(self.base_uri, data=json.dumps(payload))

        return response

    def info(self, title, message):

        title = 'INFO : {0}'.format(title)
        return self.__send_notification(title=title, message=message, color='good')

    def warn(self, title, message):

        title = 'WARN : {0}'.format(title)
        return self.__send_notification(title=title, message=message, color='warning')

    def error(self, title, message):

        title = 'ERROR : {0}'.format(title)
        return self.__send_notification(title=title, message=message, color='danger')


def main():
    try:
        webhook_url = os.environ["SLACK_WEBHOOK_URL"]

    except KeyError:
        print('ERROR: Please set the SLACK_WEB_HOOK_TOKEN AND SLACK_SUB_DOMAIN variable in your environment.')

    else:
        parser = ArgumentParser(description='slackpy command line tool')
        parser.add_argument('-c', '--channel', required=True, help='Channel')
        parser.add_argument('-t', '--title', type=str, required=False, help='Title', default='Slack Notification')
        parser.add_argument('-m', '--message', type=str, required=True, help='Message')
        parser.add_argument('-n', '--name', type=str, required=False, help='Name of Postman', default='Logger')
        parser.add_argument('-l', '--level', type=int, default=1, choices=[1, 2, 3])

        args = parser.parse_args()

        client = SlackLogger(webhook_url, args.channel, args.name)

        if args.level == 1:
            response = client.info(args.title, args.message)

        if args.level == 2:
            response = client.warn(args.title, args.message)

        if args.level == 3:
            response = client.error(args.title, args.message)

        if response.status_code == 200:
            print(True)

        else:
            print(False)

