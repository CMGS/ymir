#!/usr/bin/python
#coding:utf-8

import config
import common
from models.site import Site
from models.comment import Comment

local = {}

def generate(sid, token, node):
    table_name = '%s_%d' % (config.DEFAULT_TABLE_NAME, sid)
    database = common.dbs[node]
    comment_table = type(table_name.upper(), (Comment, ), {})
    comment_table._meta.database = database
    comment_table._meta.table_name = table_name
    local[token] = comment_table
    return comment_table

def get_table(sid, token, node):
    comment_table = local.get(token, None)
    if not comment_table:
        comment_table = generate(sid, token, node)
    return comment_table

def create(site, tid, fid, uid, ip, content):
    comment_table = get_table(site.id, site.token, site.node)
    with common.dbs[site.node].transaction():
        site.comments = Site.comments + 1
        site.save()
        comment = comment_table.create(tid=tid, fid=fid, uid=uid, ip=ip, content=content)
        if fid != 0:
            f_comment = get_comment(site.id, site.token, site.node, fid)
            f_comment.count = comment_table.count + 1
            f_comment.save()
    return comment

def get_comment(sid, token, node, id):
    comment_table = get_table(sid, token, node)
    return comment_table.get(comment_table.id == id)

def get_comments(sid, token, node, tid, expand, page, num):
    comment_table = get_table(sid, token, node)
    comments = comment_table.select().where(comment_table.tid==tid, comment_table.fid==0).paginate(page, num)
    for comment in comments:
        yield comment
        if not expand:
            continue
        for reply in get_reply_comments(sid, token, node, tid, comment.id, page, num):
            yield reply

def get_reply_comments(sid, token, node, tid, fid, page, num):
    comment_table = get_table(sid, token, node)
    return comment_table.select().where(comment_table.tid==tid, comment_table.fid==fid).paginate(page, num)

