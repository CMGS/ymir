#!/usr/bin/python
#coding:utf-8

import json
import falcon
import config
import logging

from utils import ijson
from handlers import BaseHandler
from query.up import get_up_counts, set_up_counts

logger = logging.getLevelName(__name__)

class UpComment(BaseHandler):

    def on_put(self, req, resp, token):
        site = self.get_site(token)
        cids = self.get_cids(req)

        set_up_counts(site, cids)
        resp.status = falcon.HTTP_200

    def on_get(self, req, resp, token):
        site = self.get_site(token)
        cids = self.get_cids(req)

        resp.status = falcon.HTTP_200
        resp.stream = ijson.dump(dict(zip(cids, get_up_counts(site, cids))))

    def get_cids(self, req):
        params = json.load(req.stream)
        cids = params.get('cids', None)
        if not cids or not isinstance(cids, list):
            raise falcon.HTTPBadRequest(config.HTTP_400, 'invalid params')
        return cids

