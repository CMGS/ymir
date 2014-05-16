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

BLOCK_PREFIX = 'c:b:{sid}:{ip}'
BLOCK_COUNT_PREFIX = 'c:b:c:{sid}:{page}:{num}'
BLOCK_PAGE_PREFIX = 'c:b:p:{sid}:{page}:{num}'
BLOCK_PARAMS = ['id', 'ip', 'ctime']

COMMENT_TABLE_PREFIX = 'c:{token}'
COMMENT_COUNT_PREFIX = 'c:c:{sid}:{tid}'
COMMENT_CACHE_PREFIX = 'c:o:{sid}:{id}'

COMMENT_F_PAGE_COUNT_PREFIX = 'c:f:c:{sid}:{fid}:{page}:{num}'
COMMENT_F_PAGE_PREFIX = 'c:f:p:{sid}:{fid}:{page}:{num}'

COMMENT_T_PAGE_COUNT_PREFIX = 'c:t:c:{sid}:{tid}:{expand}:{page}:{num}'
COMMENT_T_PAGE_PREFIX = 'c:t:p:{sid}:{tid}:{expand}:{page}:{num}'

COMMENT_PARAMS = ['tid', 'id', 'content', 'ip', 'ctime', 'count', 'fid']

COMMENT_UP_PREFIX = 'c:u:{sid}:{cid}'

HEAT_MAX = 3
HEAT_TIME = 20
HEAT_KEY = 'c:h:{ip}'

DEFAULT_PAGE_NUM = 20

HTTP_400 = 'Bad Request'
HTTP_403 = 'Request Forbidden'
HTTP_500 = 'Internal Error'

try:
    from local_config import *
except ImportError:
    pass

