#!/usr/bin/python
#coding:utf-8

import pickle
import config
from common import default_db
from models.site import Site, Block
from query.comment import generate

from utils.cache import rds
from utils.fn import get_node, create_obj

site_cache = {}

@default_db.commit_on_success
def create(token, name):
    site = Site.create(token = token, name = name)
    node = get_node(site.id)
    site.node = node
    site.save()
    comment_table = generate(site.id, token, node)
    comment_table.create_table()
    site_cache[token] = site
    return site

@default_db.commit_on_success
def block(site, ip):
    site.blocks = Site.blocks + 1
    site.save()
    del site_cache[site.token]
    result = Block.create(sid = site.id, ip = ip)
    rds.set(config.BLOCK_PREFIX % ip, 1)
    return result

@default_db.commit_on_success
def delete_block(site, id):
    block = Block.get(Block.id == id, Block.sid == site.id)
    rds.delete(config.BLOCK_PREFIX % block.ip)
    site.blocks = Site.blocks - 1
    site.save()
    del site_cache[site.token]
    return block.delete_instance()

def get_blocks(site, page, num):
    blocks = rds.get(config.BLOCK_COUNT_PREFIX % (site.token, page, num))
    if blocks and int(blocks) == site.blocks:
        key = config.BLOCK_PAGE_CONTENT_PREFIX % (site.token, page, num)
        result = rds.lrange(key, 0 ,-1)
        return (create_obj(r) for r in result)
    else:
        rds.set(config.BLOCK_COUNT_PREFIX % (site.token, page, num), site.blocks)
        key = config.BLOCK_PAGE_CONTENT_PREFIX % (site.token, page, num)
        rds.delete(key)
        blocks = Block.select() \
                .where(Block.sid == site.id) \
                .order_by(Block.id.desc()) \
                .paginate(page, num)
        formatter = 'id:%s:ip:%s:ctime:%s'
        def _():
            result = []
            for block in blocks:
                result.append(formatter % (block.id, block.ip, str(block.ctime)))
                yield block
            rds.rpush(key, *result)
        return _()

def check_block(sid, ip):
    if rds.get(config.BLOCK_PREFIX % ip) or \
        Block.select().where(Block.sid == sid, Block.ip == ip).first():
        rds.set(config.BLOCK_PREFIX % ip, 1)
        return True
    return False

def get_site_by_token(token):
    site = site_cache.get(token, None)
    if not site:
        site = Site.select().where(Site.token == token).first()
        site_cache[token] = site
    return site

