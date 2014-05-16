#!/usr/bin/python
#coding:utf-8

import config
from utils.cache import rds

def get_up_counts(site, cids):
    return rds.mget(*[
        config.COMMENT_UP_PREFIX.format(
            sid = site.id, \
            cid = cid, \
    ) for cid in cids])

def set_up_counts(site, cids):
    for cid in cids:
        key = config.COMMENT_UP_PREFIX.format(
            sid = site.id, \
            cid = cid, \
        )
        rds.incr(key)

