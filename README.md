# python-slack-zabbix
[![Build Status](https://travis-ci.org/PermissionData/python-slack-zabbix.svg?branch=master)](https://travis-ci.org/PermissionData/python-slack-zabbix)

## About
This script was meant to be consumed with Zabbix as a Media-Type for feedin the Slack API.  This script was inspired by ericoc's [zabbix-slack-alertscript](https://github.com/ericoc/zabbix-slack-alertscript/).  Due to the limitations of shell with JSON, this project was created.

### Versions
Works with Zabbix 2.0 and greater

## Installation

Please refer to ericoc's [README](https://github.com/ericoc/zabbix-slack-alertscript/blob/master/README.md)
for detailed instructions.  Just replace the referenced 'slack.sh' in the link with the 'slack_zabbix.py' and 'slack_zabbix.cfg' found in this repo.  Make sure that 'slack_zabbix.py' is executable
          $ chmod +x ./slack_zabbix.py

### To set up the config file:
1. Copy config sample to 'slack_zabbix.cfg'
          $ cp ./slack_zabbix.cfg.sample slack_zabbix.cfg
2. Modify the url value 'slack_zabbix.cfg' to your slack hook URL

More details to come.  But as for right now, the above link and the 2 step direction above should get you up and working.