#!/usr/bin/python
#coding:utf-8

import json
import falcon
import config
import logging

from utils import ijson
from handlers.comment import CommentBase
from query.comment import get_comments_by_fid, get_comments_by_ip

logger = logging.getLogger(__name__)

class CommentByFid(CommentBase):

    def on_get(self, req, resp, token):
        site = self.get_site(token)
        params = json.load(req.stream)

        page, num, tid = self.get_page_params(params)
        fid = int(params.get('fid', 0))

        comments = get_comments_by_fid(
            site.id, site.token, site.node, \
            tid, fid, page, num, \
        )

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

        comments = get_comments_by_ip(
            site.id, site.token, site.node, ip, tid, \
        )

        resp.status = falcon.HTTP_200
        resp.stream = ijson.dump([self.render_comment(comment) for comment in comments])

