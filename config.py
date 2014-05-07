#!/usr/bin/python
#coding:utf-8

MYSQL_DBHOST = '127.0.0.1'
MYSQL_DBPORT = '3306'
MYSQL_DBUSER = 'root'
MYSQL_DBPASS = ''
MYSQL_DBNAME = 'comment'

REPEAT_TIME = 20
DENY_TIME = 180

try:
    from local_config import *
except ImportError:
    pass

