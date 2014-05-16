#!/usr/bin/python
#coding:utf-8

import falcon
import logging
import config
from utils.heat import req_rate

from handlers.sys import Sys
from handlers.up import UpComment
from handlers.comment import Comment
from handlers.site import Site, Block
from handlers.enhance import CommentByFid, CommentByIP
from handlers.delete import DeleteCommentByIP, DeleteCommentByTid, \
        DeleteCommentByFid

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(name)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)

class HelloWorld(object):
    def on_get(self, req, resp):
        logger.info('Hello World')
        resp.status = falcon.HTTP_200
        resp.body = 'Hello World'

app = falcon.API(before=[req_rate])
app.add_route('/', HelloWorld())
app.add_route('/sys', Sys())
app.add_route('/site', Site())
app.add_route('/block', Block())
app.add_route('/m/{token}', Comment())
app.add_route('/u/{token}', UpComment())
app.add_route('/mp/{token}', CommentByIP())
app.add_route('/mf/{token}', CommentByFid())
app.add_route('/dp/{token}', DeleteCommentByIP())
app.add_route('/dt/{token}', DeleteCommentByTid())
app.add_route('/df/{token}', DeleteCommentByFid())

