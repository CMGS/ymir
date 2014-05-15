#!/usr/bin/python
#coding:utf-8

import config
from common import default_db
from models.site import Site, Block

from utils.fn import get_node
from utils.comment import generate
from utils.cache import rds, cache_page, local_cache

@default_db.commit_on_success
def create(token, name):
    site = Site.create(token = token, name = name)
    node = get_node(site.id)
    site.node = node
    site.save()
    comment_table = generate(site.id, token, node)
    comment_table.create_table()
    local_cache[token] = site
    return site

@default_db.commit_on_success
def block(site, ip):
    site.blocks = Site.blocks + 1
    site.save()
    del local_cache[site.token]
    result = Block.create(sid = site.id, ip = ip)
    rds.set(config.BLOCK_PREFIX % (site.id, ip), 1)
    return result

@default_db.commit_on_success
def delete_block(site, id):
    block = Block.get(Block.id == id, Block.sid == site.id)
    rds.delete(config.BLOCK_PREFIX % (site.id, block.ip))
    site.blocks = Site.blocks - 1
    site.save()
    del local_cache[site.token]
    return block.delete_instance()

@cache_page(
    config.BLOCK_COUNT_PREFIX, \
    config.BLOCK_PAGE_PREFIX, \
    config.BLOCK_PARAMS, \
)
def get_blocks(site, total, page, num):
    return Block.select() \
            .where(Block.sid == site.id) \
            .order_by(Block.id.desc()) \
            .paginate(page, num)

def check_block(sid, ip):
    if rds.get(config.BLOCK_PREFIX % (sid, ip)):
        return True
    elif Block.select().where(Block.sid == sid, Block.ip == ip).first():
        rds.set(config.BLOCK_PREFIX % (sid, ip), 1)
        return True
    return False

def get_site_by_token(token):
    site = local_cache.get(token, None)
    if not site:
        site = Site.select().where(Site.token == token).first()
        local_cache[token] = site
    return site

