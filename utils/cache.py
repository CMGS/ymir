#!/usr/bin/python
#coding:utf-8

import config
import msgpack
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

def cache_obj(prefix, keys):
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
                    value = msgpack.dumps([(k, getattr(obj, k, None)) for k in keys], default=str)
                rds.set(key, value)
                return obj
        return _
    return wrap

def cache_page(count_prefix, page_prefix, keys):
    def wrap(f):
        def _(site, total, page, num, *args, **kwargs):
            params = [site.token, page, num]
            params.extend(args)
            params = tuple(params)
            key = page_prefix % params
            count = rds.get(count_prefix % params)
            if count and int(count) == int(total):
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
                        result.append(msgpack.dumps([(k, getattr(d, k, None)) for k in keys], default=str))
                        yield d
                    if result:
                        rds.rpush(key, *result)
                rds.set(count_prefix % params, total)
                return iterator()
        return _
    return wrap

