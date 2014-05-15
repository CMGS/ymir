#!/usr/bin/python
#coding:utf-8

import config
import logging
from redis import Redis
from redis import ConnectionPool
from werkzeug.contrib import cache
from utils.fn import create_obj

logger = logging.getLogger(__name__)

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

local_cache = {}

def cache_obj(prefix, formatter, keys):
    def wrap(f):
        def _(site, id, *args, **kwargs):
            key = prefix % (site.token, id)
            obj = rds.get(key)
            if obj is not None:
                logger.info('get obj from cache')
                if not obj:
                    return obj
                return create_obj(obj)
            else:
                logger.info('obj cache miss')
                obj = f(site, id, *args, **kwargs)
                value = ''
                if obj:
                    value = formatter % tuple(str(getattr(obj, key)) for key in keys)
                rds.set(key, value)
                return obj
        return _
    return wrap

def cache_page(count_prefix, page_prefix, formatter, keys):
    def wrap(f):
        def _(site, total, page, num, *args, **kwargs):
            key = page_prefix % (site.token, page, num)
            count = rds.get(count_prefix % (site.token, page, num))
            if count and int(count) == total:
                logger.info('get page from cache')
                result = rds.lrange(key, 0 ,-1)
                return (create_obj(r) for r in result)
            else:
                logger.info('page cache miss')
                rds.delete(key)
                data = f(site, total, page, num, *args, **kwargs)
                def iterator():
                    result = []
                    for d in data:
                        result.append(formatter % tuple(str(getattr(d, key)) for key in keys))
                        yield d
                    rds.rpush(key, *result)
                rds.set(config.BLOCK_COUNT_PREFIX % (site.token, page, num), total)
                return iterator()
        return _
    return wrap

