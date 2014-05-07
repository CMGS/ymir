#!/usr/bin/python
#coding:utf-8

import json
import config
import falcon
import logging

from query.site import get_block, get_site_by_token
from query.comment import create

logger = logging.getLogger(__name__)

class Comment(object):

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

        try:
            #TODO perfermance
            get_block(token, ip)
        except Exception:
            pass
        else:
            logger.info('IP %s deny' % ip)
            raise falcon.HTTPForbidden(config.HTTP_403, 'ip %s deny' % ip)

        try:
            comment = create(site, tid, fid, uid, ip, content)
        except:
            logger.exception('create')
            raise falcon.HTTPInternalServerError(config.HTTP_500, 'create failed')

        resp.status = falcon.HTTP_201
        resp.body = json.dumps({'id': comment.id})

    def on_get(self, req, resp, token):
        pass

    def get_site(self, token):
        try:
            site = get_site_by_token(token)
        except Exception:
            raise falcon.HTTPNotFound()
        else:
            return site


