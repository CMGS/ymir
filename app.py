#!/usr/bin/python
#coding:utf-8

import falcon
import logging
from handlers.sys import Sys
from handlers.comment import Comment
from handlers.site import Site, Block
from handlers.enhance import CommentByFid, CommentByIP
from handlers.delete import DeleteCommentByIP, DeleteCommentByTid, \
        DeleteCommentByFid

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

class HelloWorld(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = 'Hello World'

app = falcon.API()
app.add_route('/', HelloWorld())
app.add_route('/sys', Sys())
app.add_route('/site', Site())
app.add_route('/block', Block())
app.add_route('/m/{token}', Comment())
app.add_route('/mp/{token}', CommentByIP())
app.add_route('/mf/{token}', CommentByFid())
app.add_route('/dp/{token}', DeleteCommentByIP())
app.add_route('/dt/{token}', DeleteCommentByTid())
app.add_route('/df/{token}', DeleteCommentByFid())

