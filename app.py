#!/usr/bin/python
#coding:utf-8

import falcon

class HelloWorld(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = 'Hello World'

app = falcon.API()
app.add_route('/', HelloWorld())

