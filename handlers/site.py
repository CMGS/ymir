#!/usr/bin/python
#coding:utf-8

import json
import uuid
import config
import falcon

from query.site import create, block


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
            raise falcon.HTTPInternalServerError(config.HTTP_500, 'create failed')

        resp.status = falcon.HTTP_201
        resp.body = json.dumps({'token': site.token})

class Block(object):

    def on_put(self, req, resp):
        token, ip = self.parse_params(req)

        try:
            bip = block(token, ip)
        except Exception:
            raise falcon.HTTPInternalServerError(config.HTTP_500, 'create failed')

        resp.status = falcon.HTTP_201
        resp.body = json.dumps({'id': bip.id})

    def parse_params(self, req):
        params = json.load(req.stream)
        if not params:
            raise falcon.HTTPBadRequest(config.HTTP_400, 'invalid params')

        token = params.get('token')
        ip = params.get('ip')

        if not token or not ip:
            raise falcon.HTTPBadRequest(config.HTTP_400, 'invalid params')

        return token, ip

