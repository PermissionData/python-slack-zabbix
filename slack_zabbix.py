#!/usr/bin/env python
"""slack-zabbix MODULE."""
import argparse
import syslog
import json
import yaml

import requests


def parse_configs(path):
    """Parse configuration YAML configuration file."""
    with open(path) as cfg:
        config = yaml.load(cfg.read())
    return config


def cli_args():
    """CLI Argument Parser."""
    parser = argparse.ArgumentParser(prog='zabbix slack script')
    parser.add_argument('channel', nargs=1)
    parser.add_argument('subject', nargs=1)
    parser.add_argument('body', nargs=1)
    args = parser.parse_args()
    return {
        'channel': args.channel[0],
        'subject': args.subject[0],
        'body': args.body[0]
    }


def serialize_data(**kwargs):
    """Format request body to JSON."""
    data = {
        'channel': kwargs['channel'],
        'username': 'Zabbix',
        'text': kwargs['message'],
        'icon_emoji': kwargs['emoji']
    }
    return json.dumps(data)


class SlackZabbix(object):

    """Class for Slack API and Zabbix Communication."""

    def __init__(self, config_path=None):
        """
        Construct class.

        Constructor Arguments in kwargs and configuration
        file 'slack_zabbix.cfg'.
        'slack_zabbix.cfg' must live in the same directory as the
        'slack_zabbix.py' script
        Sample configuration:
            url: https://hooks.slack.com/the/rest/of/url
            emoji:
              recovery: ':smiling:'
              problem: ':frowning:'
              default: ':simmons:'
        """
        config_path = config_path if config_path is not None \
            else './slack_zabbix.cfg'
        config = parse_configs(config_path)
        self.url = config['url']
        self.emoji = {}
        self.emoji['recovery'] = config['emoji']['recovery']
        self.emoji['problem'] = config['emoji']['problem']
        self.emoji['default'] = config['emoji']['default']

    def _set_emoji(self, subject):
        """Set emoji to use depending on the subject."""
        if 'RECOVERY' in subject:
            emoji = self.emoji['recovery']
        elif 'PROBLEM' in subject:
            emoji = self.emoji['problem']
        else:
            emoji = self.emoji['default']
        return emoji

    def send_event(self, **kwargs):
        """Send request to slack BE."""
        payload = serialize_data(**kwargs)
        i = 0
        while i < 6:
            try:
                resp = requests.post(
                    self.url,
                    data=payload,
                    timeout=5
                    )
            except requests.exceptions.Timeout:
                i += 1
                continue
            if 199 < resp.status_code < 299:
                return True, resp.content
            else:
                return False, resp.content
        return False, 'API timed out too many times'

    def broadcast(self, **kwargs):
        """Entry point function."""
        channel = kwargs.get('channel', '#general')
        subject = kwargs.get('subject', 'ERROR')
        body = kwargs.get(
            'body',
            'Zabbix did not provide a message body'
        )
        message = '{0}: {1}'.format(subject, body)
        emoji = self._set_emoji(subject)
        success, msg = self.send_event(
            emoji=emoji,
            channel=channel,
            message=message
        )
        if not success:
            syslog.syslog(
                syslog.LOG_ERR,
                'slack_zabbix.py could not successufully send'
                'message due to ==> {0}'.format(msg)
            )


if __name__ == '__main__':
    ARGS = cli_args()
    SlackZabbix().broadcast(**ARGS)
