#!/usr/bin/python
#coding:utf-8

import falcon
from utils.fn import get_node
from common import default_db
from models.site import Site, Block

from query.comment import generate

@default_db.commit_on_success
def create(token, name):
    site = Site.create(token=token, name=name)
    node = get_node(site.id)
    query = site.update(node=node)
    query.execute()
    comment_table = generate(site.id, token, node)
    comment_table.create_table()
    return site

@default_db.commit_on_success
def block(site, ip):
    query = site.update(blocks=Site.blocks + 1)
    query.execute()
    return Block.create(sid=site.id, ip=ip)

def delete_block(site, id):
    q = Block.delete().where(
            Block.id==id, Block.sid==site.id
        )
    return q.execute()

def get_blocks(sid, page, num):
    return Block.select().where(Block.sid==sid).paginate(page, num)

def get_block(sid, ip):
    return Block.select().where(Block.sid==sid, Block.ip==ip).first()

def get_site_by_token(token):
    return Site.select().where(Site.token==token).first()

