#!/usr/bin/python
#coding:utf-8

DEFAULT_DBHOST = '127.0.0.1'
DEFAULT_DBPORT = 3306
DEFAULT_DBUSER = 'root'
DEFAULT_DBPASS = ''
DEFAULT_DBNAME = 'comment'

STORE = [
    {
        'host':'127.0.0.1', \
        'port':3306, \
        'user':'root', \
        'password':'', \
        'database':'comment', \
    }, \
]

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = ''
REDIS_POOL_SIZE = 100

REPEAT_TIME = 20
DENY_TIME = 180

try:
    from local_config import *
except ImportError:
    pass

