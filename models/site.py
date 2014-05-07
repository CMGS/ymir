#!/usr/bin/python
#coding:utf-8

import peewee
import datetime
from common import default_db, StaticCharField

class Site(peewee.Model):

    class Meta:
        database = default_db

    id = peewee.PrimaryKeyField()
    token = StaticCharField(unique=True, max_length=32)
    name = peewee.CharField(null=False, max_length=64)
    ctime = peewee.DateTimeField(default=datetime.datetime.now)
    topics = peewee.BigIntegerField(default=0)
    blocks = peewee.BigIntegerField(default=0)

class Block(peewee.Model):

    class Meta:
        database = default_db

    id = peewee.PrimaryKeyField()
    sid = peewee.IntegerField(null=False, index=True)
    ip = peewee.CharField(max_length=15)
    ctime = peewee.DateTimeField(default=datetime.datetime.now)

