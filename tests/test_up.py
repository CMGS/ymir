#!/usr/bin/python
#coding:utf-8

import json
import falcon
import config

from utils.cache import rds

from tests.base import is_iter
from tests.base import TestBase
from query.site import get_site_by_token

class TestUpComment(TestBase):

    def setUp(self):
        super(TestUpComment, self).setUp()
        self.path = '/u/%s' % self.token
        self.site = get_site_by_token(self.token)

    def test_set_up_counts(self):
        r = range(15, 17)
        self.send_request(
            path = self.path, method = 'PUT', data = json.dumps({'cids': r})
        )

        self.assertEqual(falcon.HTTP_200, self.mock.status)
        for i in r:
            k = config.COMMENT_UP_PREFIX.format(sid = self.site.id, cid = i)
            self.assertEqual(int(rds.get(k)), 1)

    def test_get_up_counts(self):
        r = range(17, 19)
        for i in r:
            k = config.COMMENT_UP_PREFIX.format(sid = self.site.id, cid = i)
            rds.incr(k)

        response = self.send_request(
            path = self.path, method = 'GET', data = json.dumps({'cids': r})
        )

        self.assertEqual(falcon.HTTP_200, self.mock.status)
        self.assertTrue(is_iter(response))
        data = json.loads(''.join(response))
        self.assertIsInstance(data, dict)
        for i in r:
            self.assertTrue(data.get(str(i)))
            self.assertEqual(int(data[str(i)]), 1)

    def test_params_invaild(self):
        self._test_bad_request(self.path, 'PUT')
        self._test_bad_request(self.path, 'GET')

