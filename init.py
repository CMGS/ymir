#!/usr/bin/python
#coding:utf-8

import logging
from models.site import Site, Block

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

Site.create_table(fail_silently=True)
Block.create_table(fail_silently=True)

