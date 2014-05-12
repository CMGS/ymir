#!/usr/bin/python
#coding:utf-8

import peewee
import datetime

class Comment(peewee.Model):

    id = peewee.PrimaryKeyField()
    tid = peewee.IntegerField(null=False, index=True)
    fid = peewee.IntegerField(null=False, index=True, default=0)
    uid = peewee.IntegerField(null=False, index=True, default=0)
    ip = peewee.CharField(max_length=15, null=False, index=True)
    count = peewee.IntegerField(null=False, default=0)
    content = peewee.TextField(null=False)
    ctime = peewee.DateTimeField(default=datetime.datetime.now)

