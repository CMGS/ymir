#!/usr/bin/python
#coding:utf-8

import json
import falcon

from tests.base import is_iter
from tests.base import TestBase

def fake_create(*args, **kwargs):
    raise Exception('this is test')

class TestSite(TestBase):

    def test_create_site(self):
        response = self.send_request(path='/site', data=json.dumps({'name': 'test'}))

        self.assertTrue(is_iter(response))
        self.assertEqual(falcon.HTTP_201, self.mock.status)
        data = json.loads(''.join(response))
        self.assertIsInstance(data, dict)
        token = data.get('token')
        self.assertTrue(token)
        self.assertIsInstance(token, (str, unicode))
        self.assertEqual(len(token), 32)

        self._test_bad_request('/site', 'PUT')

    def test_create_500(self):
        from handlers import site
        self.patch(site, 'create', fake_create)

        self.send_request(path='/site', data=json.dumps({'name': 'test'}))
        self.assertEqual(falcon.HTTP_500, self.mock.status)

