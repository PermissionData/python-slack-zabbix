#!/user/bin/env python
"""Unit Test for slack-zabbix."""
import unittest
import json

from slack_zabbix import SlackZabbix, serialize_data

class TestFormatRequest(unittest.TestCase):
    """Unit test for format_request function."""

    def setUp(self):
        self.sz = SlackZabbix()


    def test_happy_path(self):
        kwargs = {
            'message': 'Trigger: fake\nServerity: high\n12345',
            'channel': '#test',
            'emoji': ':smiling:'
        }
        formatted_request = serialize_data(**kwargs)
        self.assertEquals(
            json.loads(formatted_request),
            json.loads(
                '{"channel": "#test", "username": "Zabbix", "text": "Trigger: '
                'fake\\nServerity: high\\n12345", "icon_emoji": ":smiling:"}'
            )
        )


    def test_overloaded_kwargs(self):
        kwargs = {
            'message': 'Trigger: fake\nServerity: high\n12345',
            'channel': '#test',
            'emoji': ':smiling:',
            'something_unnecessary': 'foo',
            'something_else_unnecessary': 'bar'
        }
        formatted_request = serialize_data(**kwargs)
        self.assertEquals(
            json.loads(formatted_request),
            json.loads(
                '{"channel": "#test", "username": "Zabbix", "text": "Trigger: '
                'fake\\nServerity: high\\n12345", "icon_emoji": ":smiling:"}'
            )
        )


    def test_insufficient_kwargs(self):
        kwargs = {
            'message': 'fake\nServerity: high\n12345',
            'emoji': ':smiling:'
        }
        with self.assertRaises(KeyError):
            serialize_data(**kwargs)

        kwargs = {
            'channel': '#test',
            'emoji': ':smiling:'
        }
        with self.assertRaises(KeyError):
            serialize_data(**kwargs)
        with self.assertRaises(KeyError):
            serialize_data(emoji=':smiling:')


    def test_problem_emoji(self):
        kwargs = {
            'message': 'Trigger: fake\nServerity: high\n12345',
            'channel': '#test',
            'emoji': self.sz.emoji['problem']
        }
        formatted_request = serialize_data(**kwargs)
        self.assertEquals(
            json.loads(formatted_request),
            json.loads(
                '{"channel": "#test", "username": "Zabbix", "text": "Trigger: '
                'fake\\nServerity: high\\n12345", "icon_emoji": ":frowning:"}'
            )
        )

    def test_recovery_emoji(self):
        kwargs = {
            'message': 'Trigger: fake\nServerity: high\n12345',
            'channel': '#test',
            'emoji': self.sz.emoji['recovery']
        }
        formatted_request = serialize_data(**kwargs)
        self.assertEquals(
            json.loads(formatted_request),
            json.loads(
                '{"channel": "#test", "username": "Zabbix", "text": "Trigger: '
                'fake\\nServerity: high\\n12345", "icon_emoji": ":smiling:"}'
            )
        )

    def test_default_emoji(self):
        kwargs = {
            'message': 'Trigger: fake\nServerity: high\n12345',
            'channel': '#test',
            'emoji': self.sz.emoji['default']
        }
        formatted_request = serialize_data(**kwargs)
        self.assertEquals(
            json.loads(formatted_request),
            json.loads(
                '{"channel": "#test", "username": "Zabbix", "text": "Trigger: '
                'fake\\nServerity: high\\n12345", "icon_emoji": ":zap:"}'
            )
        )
