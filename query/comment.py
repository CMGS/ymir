#!/usr/bin/python
#coding:utf-8

import config
import common
from models.comment import Comment

local = {}

def generate(site, node):
    table_name = '%s_%d' % (config.DEFAULT_TABLE_NAME, site.id)
    database = common.dbs[node]

    site_comment = type(table_name.upper(), (Comment, ), {})
    site_comment._meta.database = database
    site_comment._meta.table_name = table_name
    site_comment.create_table()
    local[site.token] = site_comment

