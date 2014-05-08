#!/usr/bin/python
#coding:utf-8

from json import JSONEncoder
from common import dbs_mod, dbs_len

def get_node(id):
    while id % dbs_mod != id:
        id = id % dbs_mod

    id %= dbs_len
    return id

def json(data):
    return JSONEncoder.iterencode(data)

