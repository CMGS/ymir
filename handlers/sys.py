#!/usr/bin/python
#coding:utf-8

import config
import falcon
import logging

from utils import ijson
from handlers import BaseHandler

logger = logging.getLogger(__name__)

class Sys(BaseHandler):

    def on_get(self, req, resp):
        result = {'default_db':[], 'redis':[]}
        for k in dir(config):
            if k.startswith('DEFAULT_DB'):
                result['default_db'].append(getattr(config, k))
            elif k.startswith('REDIS_'):
                result['redis'].append(getattr(config, k))
        result['store'] = config.STORE
        resp.status = falcon.HTTP_200
        resp.stream = ijson.dump(result)

