#!/usr/bin/python
#coding:utf-8

import logging
from models.app import App, Block

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

App.create_table()
Block.create_table()

