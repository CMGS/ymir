#!/usr/bin/python
#coding:utf-8

import json
import falcon
import config
import logging

from handlers import BaseHandler
from query.comment import delete_comment, get_comments_by_ip

logger = logging.getLogger(__name__)

class DeleteCommentByIP(BaseHandler):

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

