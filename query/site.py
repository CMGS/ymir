#!/usr/bin/python
#coding:utf-8

from utils.fn import get_node
from common import default_db
from models.site import Site, Block

@default_db.commit_on_success
def create(token, name):
    site = Site.create(token=token, name=name)
    node = get_node(site.id)
    query = site.update(node=node)
    query.execute()
    return site

@default_db.commit_on_success
def block(token, ip):
    site = get_site_by_token(token)
    query = site.update(blocks=Site.blocks + 1)
    query.execute()
    return Block.create(sid=site.id, ip=ip)

def delete_block(token, id):
    site = get_site_by_token(token)
    block = Block.get(Block.id==id).get(Block.sid==site.id)
    return block.delete_instance()

def get_blocks(token, page, num):
    site = get_site_by_token(token)
    return Block.select().where(Block.sid==site.id).paginate(page, num)

def get_site_by_token(token):
    return Site.get(Site.token==token)

