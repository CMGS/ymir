#!/usr/bin/python
#coding:utf-8

import config
import common
from models.comment import Comment
from utils.cache import local_cache

def generate(sid, token, node):
    table_name = '%s_%d' % (config.DEFAULT_TABLE_NAME, sid)
    database = common.dbs[node]
    comment_table = type(table_name.upper(), (Comment, ), {})
    comment_table._meta.database = database
    comment_table._meta.table_name = table_name
    local_cache[config.COMMENT_TABLE_PREFIX.format(token = token)] = comment_table
    return comment_table

def get_table(sid, token, node):
    comment_table = local_cache.get(config.COMMENT_TABLE_PREFIX.format(token = token), None)
    if not comment_table:
        comment_table = generate(sid, token, node)
    return comment_table

def cross_transactions(f):
    def _(site, *args):
        common.default_db.set_autocommit(False)
        common.dbs[site.node].set_autocommit(False)
        try:
            result = f(site, *args)
            common.default_db.commit()
            common.dbs[site.node].commit()
            return result
        except Exception:
            common.default_db.rollback()
            common.dbs[site.node].rollback()
            raise
        finally:
            common.default_db.set_autocommit(True)
            common.dbs[site.node].set_autocommit(True)
    return _

