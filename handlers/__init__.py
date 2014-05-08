#!/usr/bin/python
#coding:utf-8

import falcon
from query.site import get_site_by_token

class BaseHandler(object):

    def get_site(self, token):
        site = get_site_by_token(token)
        if not site:
            raise falcon.HTTPNotFound()
        return site

