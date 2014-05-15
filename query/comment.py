#!/usr/bin/python
#coding:utf-8

import config
from models.site import Site

from utils.cache import rds, cache_page, cache_obj
from utils.comment import cross_transactions, get_table

@cross_transactions
def create(site, tid, fid, uid, ip, content):
    comment_table = get_table(site.id, site.token, site.node)
    site.comments = Site.comments + 1
    site.save()
    comment = comment_table.create(tid=tid, fid=fid, uid=uid, ip=ip, content=content)
    if fid:
        f_comment = get_comment(site, fid)
        f_comment.count = comment_table.count + 1
        f_comment.save()
        rds.delete(config.COMMENT_CACHE_PREFIX % (site.token, fid))
    rds.incr(config.COMMENT_COUNT_PREFIX % (site.token, tid))
    return comment

@cross_transactions
def delete_comment(site, id):
    comment_table = get_table(site.id, site.token, site.node)
    instance = comment_table.get(comment_table.id == id)
    instance.delete_instance()
    result = comment_table.delete().where(comment_table.fid == id).execute()
    if instance.fid:
        f_comment = get_comment(site, instance.fid)
        f_comment.count = comment_table.count - 1
        f_comment.save()
        rds.delete(config.COMMENT_CACHE_PREFIX % (site.token, instance.fid))
    result += 1
    site.comments = Site.comments - result
    site.save()
    rds.decr(config.COMMENT_COUNT_PREFIX % (site.token, instance.tid), result)
    return result

@cross_transactions
def delete_comments_by_tid(site, tid):
    comment_table = get_table(site.id, site.token, site.node)
    result = comment_table.delete().where(comment_table.tid == tid).execute()
    site.comments = Site.comments - result
    site.save()
    rds.decr(config.COMMENT_COUNT_PREFIX % (site.token, tid), result)
    return result

@cross_transactions
def delete_comments_by_fid(site, fid):
    comment_table = get_table(site.id, site.token, site.node)
    f_comment = get_comment(site, fid)
    result = comment_table.delete().where(comment_table.fid == fid).execute()
    f_comment.count = comment_table.count - result
    f_comment.save()
    site.comments = Site.comments - result
    site.save()
    rds.decr(config.COMMENT_COUNT_PREFIX % (site.token, f_comment.tid), result)
    return result

#FIXME TOOOOOO SLOW, NOT CACHED
def get_comments_by_ip(site, ip, tid = -1):
    comment_table = get_table(site.id, site.token, site.node)
    if tid == -1:
        comments = comment_table.select().where(comment_table.ip == ip)
    else:
        comments = comment_table.select().where(comment_table.tid == tid, comment_table.ip == ip)
    return comments

def get_comments_by_tid(site, tid, expand, page, num):
    key = config.COMMENT_COUNT_PREFIX % (site.token, tid)
    # We don't care the count, just notify renew page cache
    t_count = rds.get(key) or 0
    return get_comments(site, t_count, page, num, tid, expand)

@cache_page(
    config.COMMENT_F_PAGE_COUNT_PREFIX, \
    config.COMMENT_F_PAGE_PREFIX, \
    config.COMMENT_PARAMS, \
)
def get_comments_by_fid(site, count, page, num, fid):
    comment_table = get_table(site.id, site.token, site.node)
    return comment_table \
            .select() \
            .where(comment_table.fid == fid) \
            .order_by(comment_table.id.desc()) \
            .paginate(page, num)

@cache_page(
    config.COMMENT_T_PAGE_COUNT_PREFIX, \
    config.COMMENT_T_PAGE_PREFIX, \
    config.COMMENT_PARAMS, \
)
def get_comments(site, count, page, num, tid, expand):
    comment_table = get_table(site.id, site.token, site.node)
    comments = comment_table \
                .select() \
                .where(comment_table.tid == tid, comment_table.fid == 0) \
                .order_by(comment_table.id.desc()) \
                .paginate(page, num)
    for comment in comments:
        yield comment
        if not expand:
            continue
        for reply in get_comments_by_fid(site, comment.count, page, num, comment.id):
            yield reply

@cache_obj(
    config.COMMENT_CACHE_PREFIX, \
    config.COMMENT_PARAMS, \
)
def get_comment_cached(site, id):
    comment_table = get_table(site.id, site.token, site.node)
    f_comment = comment_table.select().where(comment_table.id == id).first()
    return f_comment

#internal use
def get_comment(site, id):
    comment_table = get_table(site.id, site.token, site.node)
    return comment_table.get(comment_table.id == id)

