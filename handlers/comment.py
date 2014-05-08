#!/usr/bin/python
#coding:utf-8

import json
import config
import falcon
import logging
from collections import OrderedDict

from handlers import BaseHandler
from query.site import get_block
from query.comment import create, get_comments

logger = logging.getLogger(__name__)

class Comment(BaseHandler):

    def on_put(self, req, resp, token):
        site = self.get_site(token)
        msg = json.load(req.stream)

        tid = msg.get('tid', 0)
        fid = msg.get('fid', 0)
        uid = msg.get('uid', 0)
        ip = msg.get('ip', 0)
        content = msg.get('content', None)

        if not tid or not uid or not ip or not content:
            raise falcon.HTTPBadRequest(config.HTTP_400, 'invalid params')

        #HEAT PROTECT
        #CACHE FOR LONG TIME
        if get_block(site.id. ip):
            logger.info('IP %s deny' % ip)
            raise falcon.HTTPForbidden(config.HTTP_403, 'ip %s deny' % ip)

        try:
            comment = create(site, tid, fid, uid, ip, content)
        except Exception:
            logger.exception('create comment')
            raise falcon.HTTPInternalServerError(config.HTTP_500, 'create comment failed')

        resp.status = falcon.HTTP_201
        resp.body = json.dumps({'id': comment.id})

    def on_get(self, req, resp, token):
        site = self.get_site(token)
        params = json.load(req.stream)

        page = int(params.get('page', 0))
        tid = int(params.get('tid', 0 ))
        if page < 1:
            raise falcon.HTTPBadRequest(config.HTTP_400, 'invalid params')
        num = int(params.get('num', config.DEFAULT_PAGE_NUM))
        expand = bool(params.get('expand', 0))

        comments = get_comments(
            site.id, site.token, site.node, \
            tid, expand, page, num
        )

        resp.status = falcon.HTTP_200

        if not expand:
            resp.body = self.render_comments_without_expand(comments)
        else:
            resp.body = self.render_comments_with_expand(comments)

    def render_comments_with_expand(self, comments):
        result = OrderedDict()
        for comment in comments:
            if comment.fid and result.get(comment.fid):
                result[comment.fid].append(self.render_comment(comment))
                continue
            result[comment.id] = [self.render_comment(comment)]
        return json.dumps(result.values())

    def render_comments_without_expand(self, comments):
        return json.dumps(
            [self.render_comment(comment) for comment in comments]
        )


    def render_comment(self, comment):
        return {
                   'id':comment.id, \
                   'content':comment.content, \
                   'ip':comment.ip, \
                   'ctime':str(comment.ctime), \
               }