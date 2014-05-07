#!/usr/bin/python
#coding:utf-8

import config
import peewee

conn = peewee.MySQLDatabase(
    config.MYSQL_DBNAME, \
    host = config.MYSQL_DBHOST, \
    port = config.MYSQL_DBPORT, \
    user = config.MYSQL_DBUSER, \
    password = config.MYSQL_DBPASS, \
)

