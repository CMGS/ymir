#!/usr/bin/python
#coding:utf-8

import json
import config
import falcon
import logging
from collections import OrderedDict

from utils import ijson
from handlers import BaseHandler
from query.site import check_block
from query.comment import create, get_comments_by_tid, \
        delete_comment, get_comment_cached

logger = logging.getLogger(__name__)

class CommentBase(BaseHandler):

    def get_page_params(self, params):
        page = int(params.get('page', 0))
        num = int(params.get('num', config.DEFAULT_PAGE_NUM))
        tid = int(params.get('tid', 0))
        if page < 1 or num < 0 or not tid:
            raise falcon.HTTPBadRequest(config.HTTP_400, 'invalid params')
        return page, num, tid

    def render_comments(self, comments, fid=0):
        result = OrderedDict()
        for comment in comments:
            if comment.fid == fid:
                result[comment.id] = [self.render_comment(comment)]
            else:
                result[comment.fid].append(self.render_comment(comment))
        return ijson.dump(result.values())

    def render_comment(self, comment):
        return {
                    'tid': comment.tid, \
                    'id':comment.id, \
                    'content':comment.content, \
                    'ip':comment.ip, \
                    'ctime':str(comment.ctime), \
                    'count':comment.count, \
               }

class Comment(CommentBase):

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

        if check_block(site.id, ip):
            logger.info('IP %s deny' % ip)
            raise falcon.HTTPForbidden(config.HTTP_403, 'ip %s deny' % ip)

        try:
            comment = create(site, tid, fid, uid, ip, content)
        except Exception:
            logger.exception('create comment')
            raise falcon.HTTPInternalServerError(config.HTTP_500, 'create comment failed')

        resp.status = falcon.HTTP_201
        resp.stream = ijson.dump({'id': comment.id})

    def on_get(self, req, resp, token):
        site = self.get_site(token)
        params = json.load(req.stream)

        page, num, tid = self.get_page_params(params)
        expand = params.get('expand', 0)

        comments = get_comments_by_tid(site, tid, expand, page, num)

        resp.status = falcon.HTTP_200
        resp.stream = self.render_comments(comments)

    def on_delete(self, req, resp, token):
        site = self.get_site(token)
        params = json.load(req.stream)

        id = int(params.get('id', 0))
        if not id:
            raise falcon.HTTPBadRequest(config.HTTP_400, 'invalid params')

        comment = get_comment_cached(site, id)
        if not comment:
            raise falcon.HTTPNotFound()

        try:
            delete_comment(site, comment)
        except Exception:
            logger.exception('delete')
            raise falcon.HTTPInternalServerError(config.HTTP_500, 'delete comment failed')

        resp.status = falcon.HTTP_200

