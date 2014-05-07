#!/usr/bin/python
#coding:utf-8

import json
import uuid
import config
import falcon
import logging

from query.site import create, block, \
        delete_block, get_blocks

logger = logging.getLogger(__name__)

class Site(object):

    def on_put(self, req, resp):
        params = json.load(req.stream)
        if not params or not params.get('name'):
            raise falcon.HTTPBadRequest(config.HTTP_400, 'invalid params')

        token = uuid.uuid4().hex
        name = params.get('name')

        try:
            site = create(token, name)
        except Exception:
            logger.exception('create')
            raise falcon.HTTPInternalServerError(config.HTTP_500, 'create failed')

        resp.status = falcon.HTTP_201
        resp.body = json.dumps({'token': site.token})

class Block(object):

    def on_put(self, req, resp):
        token, ip, _ = self.parse_params(req)

        try:
            bip = block(token, ip)
        except Exception:
            logger.exception('create')
            raise falcon.HTTPInternalServerError(config.HTTP_500, 'create failed')

        resp.status = falcon.HTTP_201
        resp.body = json.dumps({'id': bip.id})

    def on_delete(self, req, resp):
        token, id, _ = self.parse_params(req, 'id')

        try:
            delete_block(token, id)
        except Exception:
            raise falcon.HTTPNotAcceptable('block or site not exists')

        resp.status = falcon.HTTP_200

    def on_get(self, req, resp):
        token, page, params = self.parse_params(req, 'page')
        page = int(page)
        if page < 1:
            raise falcon.HTTPBadRequest(config.HTTP_400, 'invalid params')
        num = int(params.get('num', config.DEFAULT_PAGE_NUM))

        try:
            blocks = get_blocks(token, page, num)
        except Exception:
            resp.status = falcon.HTTP_204
            raise falcon.HTTPNotAcceptable('no blocks')

        resp.status = falcon.HTTP_200
        resp.body = json.dumps([{'ip':block.ip, 'ctime':str(block.ctime)} for block in blocks])

    def parse_params(self, req, data='ip'):
        params = json.load(req.stream)
        if not params:
            raise falcon.HTTPBadRequest(config.HTTP_400, 'invalid params')

        token = params.get('token')
        data = params.get(data)

        if not token or not data:
            raise falcon.HTTPBadRequest(config.HTTP_400, 'invalid params')

        return token, data, params

