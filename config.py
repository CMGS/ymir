#!/usr/bin/python
#coding:utf-8

DEBUG = False

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

BLOCK_PREFIX = 'comment:block:ip:%s:%s'
BLOCK_COUNT_PREFIX = 'comment:block:count:%s:%s:%s'
BLOCK_PAGE_PREFIX = 'comment:block:page:%s:%s:%s'
BLOCK_PARAMS = ['id', 'ip', 'ctime']

COMMENT_TABLE_PREFIX = 'comment:%s'
COMMENT_COUNT_PREFIX = 'comment:count:%s:%s'
COMMENT_CACHE_PREFIX = 'comment:cache:%s:%s'

COMMENT_F_PAGE_COUNT_PREFIX = 'comment:f:page:count:%s:%s:%s:%s'
COMMENT_F_PAGE_PREFIX = 'comment:f:page:%s:%s:%s:%s'

COMMENT_T_PAGE_COUNT_PREFIX = 'comment:t:page:count:%s:%s:%s:%s:%s'
COMMENT_T_PAGE_PREFIX = 'comment:t:page:%s:%s:%s:%s:%s'

COMMENT_PARAMS = ['tid', 'id', 'content', 'ip', 'ctime', 'count', 'fid']

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

