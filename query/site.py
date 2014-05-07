#!/usr/bin/python
#coding:utf-8

from models.site import Site, Block

def create(token, name):
    return Site.create(token=token, name=name)

def block(token, ip):
    site = get_site_by_token(token)
    if not site:
        raise Exception('no site')
    return Block.create(sid=site.id, ip=ip)

def get_site_by_token(token):
    try:
        site = Site.select().where(Site.token==token).get()
    except Site.DoesNotExist:
        site = None
    return site

