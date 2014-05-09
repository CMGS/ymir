#!/usr/bin/python
#coding:utf-8

DEFAULT_DBHOST = '127.0.0.1'
DEFAULT_DBPORT = 3306
DEFAULT_DBUSER = 'root'
DEFAULT_DBPASS = ''
DEFAULT_DBNAME = 'comment_test'

DEFAULT_TABLE_NAME = 'comment'

STORE = [
    {
        'host':'127.0.0.1', \
        'port':3306, \
        'user':'root', \
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

