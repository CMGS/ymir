#!/usr/bin/python
#coding:utf-8

import json
import falcon
import config
import logging

from utils import ijson
from handlers.comment import CommentBase
from query.comment import get_comments_by_fid, get_comments_by_ip, \
        delete_comment

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

class DeleteCommentByTid(CommentBase):

    def on_delete(self, req, resp, token):
        pass

class DeleteCommentByFid(CommentBase):

    def on_delete(self, req, resp, token):
        pass

class DeleteCommentByIP(CommentBase):

    def on_delete(self, req, resp, token):
        site = self.get_site(token)
        params = json.load(req.stream)

        ip = params.get('ip', None)
        tid = int(params.get('tid', -1))
        if not ip:
            raise falcon.HTTPBadRequest(config.HTTP_400, 'invalid params')

        try:
            # Because this method will update comment table
            # and Father comment if fid is not 0
            # That's why this method tooooo slow for large data
            comments = get_comments_by_ip(
                site.id, site.token, site.node, ip, tid, \
            )
            f_comments = []
            for comment in comments:
                if comment.fid != 0:
                    delete_comment(site, comment.id)
                    continue
                f_comments.append(comment)
            for comment in f_comments:
                delete_comment(site, comment.id)
        except Exception:
            logger.exception('delete')
            raise falcon.HTTPInternalServerError(config.HTTP_500, 'delete comment failed')

        resp.status = falcon.HTTP_200

