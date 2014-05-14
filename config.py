#!/usr/bin/python
#coding:utf-8

DEBUG = True

DEFAULT_DBHOST = '127.0.0.1'
DEFAULT_DBPORT = 3306
DEFAULT_DBUSER = 'root'
DEFAULT_DBPASS = ''
DEFAULT_DBNAME = 'comment'

DEFAULT_TABLE_NAME = 'comment'

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
REDIS_PREFIX = 'comment:cache:'

DEFAULT_REDIS_EXPIRE = 86400
BLOCK_PREFIX = 'comment:block:ip:%s'

REPEAT_TIME = 20
DENY_TIME = 180

DEFAULT_PAGE_NUM = 20

HTTP_400 = 'Bad Request'
HTTP_403 = 'Request Forbidden'
HTTP_500 = 'Internal Error'

try:
    from local_config import *
except ImportError:
    pass

