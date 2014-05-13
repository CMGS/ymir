#!/usr/bin/python
#coding:utf-8

from json import _default_encoder

def dump(obj):
    iterable = _default_encoder.iterencode(obj)

    for chunk in iterable:
        if isinstance(chunk, unicode):
            chunk = chunk.encode('utf8')
        yield chunk

