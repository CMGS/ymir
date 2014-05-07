#!/usr/bin/python
#coding:utf-8

import config
import peewee

peewee.QueryCompiler.field_map['char'] = 'CHAR'

class StaticCharField(peewee.CharField):
    db_field = 'char'

default_db = peewee.MySQLDatabase(
    database = config.DEFAULT_DBNAME, \
    host = config.DEFAULT_DBHOST, \
    port = config.DEFAULT_DBPORT, \
    user = config.DEFAULT_DBUSER, \
    password = config.DEFAULT_DBPASS, \
)

dbs = [peewee.MySQLDatabase(**params) for params in config.STORE]
dbs_len = len(dbs)
dbs_mod = 10**dbs_len

