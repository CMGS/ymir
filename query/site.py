#!/usr/bin/python
#coding:utf-8

from models.site import Site, Block

def create(token, name):
    return Site.create(token=token, name=name)

def block(token, ip):
    site = get_site_by_token(token)
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

