#!/usr/bin/python
#coding:utf-8

import json
import falcon
import logging

from query.comment import get_comments
from handlers.comment import CommentBase

logger = logging.getLogger(__name__)

class CommentByFid(CommentBase):

    def on_get(self, req, resp, token):
        site = self.get_site(token)
        params = json.load(req.stream)

        page, num, tid = self.get_page_params(params)
        fid = int(params.get('fid', 0))

        comments = get_comments(
            site.id, site.token, site.node, \
            tid, 0, page, num, fid=fid, \
        )

        resp.status = falcon.HTTP_200
        resp.stream = self.render_comments(comments, fid=fid)

