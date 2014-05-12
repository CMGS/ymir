#!/usr/bin/python
#coding:utf-8

from utils.fn import get_node
from common import default_db
from models.site import Site, Block

from query.comment import generate

@default_db.commit_on_success
def create(token, name):
    site = Site.create(token = token, name = name)
    node = get_node(site.id)
    site.node = node
    site.save()
    comment_table = generate(site.id, token, node)
    comment_table.create_table()
    return site

@default_db.commit_on_success
def block(site, ip):
    site.blocks = Site.blocks + 1
    site.save()
    return Block.create(sid = site.id, ip = ip)

@default_db.commit_on_success
def delete_block(site, id):
    site.blocks = Site.blocks - 1
    site.save()
    return Block.delete().where(
        Block.id == id, Block.sid == site.id
    ).execute()

def get_blocks(sid, page, num):
    return Block.select().where(Block.sid == sid).paginate(page, num)

def get_block(sid, ip):
    return Block.select().where(Block.sid == sid, Block.ip == ip).first()

def get_site_by_token(token):
    return Site.select().where(Site.token == token).first()

