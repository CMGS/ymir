#!/usr/bin/python
#coding:utf-8

import falcon
import config
from utils.cache import rds

def req_rate(req, resp, params):
    ip = req.get_header('X-Real-IP')
    if not ip:
        return
    key = config.HEAT_KEY.format(ip = ip)
    current = rds.get(key)
    if current and int(current) > config.HEAT_MAX:
        raise falcon.HTTPForbidden(config.HTTP_403, 'ip %s overheat' % ip)

    if not current:
        rds.incr(key)
        rds.expire(key, config.HEAT_TIME)
    else:
        rds.incr(key)

