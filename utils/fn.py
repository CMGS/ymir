#!/usr/bin/python
#coding:utf-8

import msgpack
from common import dbs_mod, dbs_len

def get_node(id):
    while id % dbs_mod != id:
        id = id % dbs_mod

    id %= dbs_len
    return id

class Obj(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

def create_obj(data):
    data = msgpack.unpackb(data)
    return Obj(**dict(data))

