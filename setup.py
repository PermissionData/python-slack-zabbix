#!/user/bin/env python
"""slack-zabbix MODULE """
from setuptools import setup

setup(
    name="slack-zabbix",
    version="0.1.0",
    description="Zabbix Script for Slack",
    license="MIT",
    install_requires=["requests", "pyyaml"],
    author="Allan Liu",
    author_email="aliu@permissiondata.com",
    url="http://github.com/permissiondata/python-slack-zabbix"
)
