#!/usr/bin/python
#coding:utf-8

import json
import falcon
import config
import logging

from utils import ijson
from handlers.comment import CommentBase
from query.comment import get_comments_by_fid, \
        get_comments_by_ip, get_comment_cached

logger = logging.getLogger(__name__)

class CommentByFid(CommentBase):

    def on_get(self, req, resp, token):
        site = self.get_site(token)
        params = json.load(req.stream)

        page = int(params.get('page', 0))
        num = int(params.get('num', config.DEFAULT_PAGE_NUM))
        fid = int(params.get('fid', -1))
        if page < 1 or num < 0 or fid < 0:
            raise falcon.HTTPBadRequest(config.HTTP_400, 'invalid params')

        f_comment = get_comment_cached(site, fid)
        if not f_comment:
            raise falcon.HTTPNotFound()
        comments = get_comments_by_fid(site, f_comment.count, page, num, fid = f_comment.id)

        resp.status = falcon.HTTP_200
        resp.stream = ijson.dump([self.render_comment(comment) for comment in comments])

class CommentByIP(CommentBase):

    def on_get(self, req, resp, token):
        site = self.get_site(token)
        params = json.load(req.stream)

        ip = params.get('ip', None)
        tid = int(params.get('tid', -1))
        if not ip:
            raise falcon.HTTPBadRequest(config.HTTP_400, 'invalid params')

        comments = get_comments_by_ip(site, ip, tid)

        resp.status = falcon.HTTP_200
        resp.stream = ijson.dump([self.render_comment(comment) for comment in comments])

