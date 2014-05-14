#!/usr/bin/python
#coding:utf-8

import config
from redis import Redis
from redis import ConnectionPool
from werkzeug.contrib import cache

redis_pool = ConnectionPool(
    host = config.REDIS_HOST, \
    port = config.REDIS_PORT, \
    db = config.REDIS_DB, \
    password = config.REDIS_PASSWORD, \
    max_connections = config.REDIS_POOL_SIZE, \
)

rds = Redis(connection_pool = redis_pool)

backend = cache.RedisCache(
    host = rds, \
    default_timeout = config.DEFAULT_REDIS_EXPIRE, \
    key_prefix = config.REDIS_PREFIX, \
)

