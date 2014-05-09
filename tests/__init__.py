#!/usr/bin/python
#coding:utf-8

DEFAULT_DBHOST = 'git.hunantv.com'
DEFAULT_DBPORT = 3306
DEFAULT_DBUSER = 'test'
DEFAULT_DBPASS = ''
DEFAULT_DBNAME = 'comment_test'

DEFAULT_TABLE_NAME = 'comment'

STORE = [
    {
        'host':'git.hunantv.com', \
        'port':3306, \
        'user':'test', \
        'password':'', \
        'database':'comment_test', \
    }, \
]

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = ''
REDIS_POOL_SIZE = 100
REDIS_PRFIX = 'comment_test'

try:
    from tests.local_config import *
except ImportError:
    pass

