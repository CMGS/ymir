#!/usr/bin/python
#coding:utf-8

import json
import falcon

from handlers import site
from tests.base import is_iter
from tests.base import TestBase
from tests.base import fake_func

class TestSite(TestBase):

    def test_create_site(self):
        response = self.send_request(
            path = '/site', data = json.dumps({'name': 'test'})
        )

        self.assertTrue(is_iter(response))
        self.assertEqual(falcon.HTTP_201, self.mock.status)
        data = json.loads(''.join(response))
        self.assertIsInstance(data, dict)
        token = data.get('token')
        self.assertTrue(token)
        self.assertIsInstance(token, (str, unicode))
        self.assertEqual(len(token), 32)

        self._test_bad_request('/site', 'PUT')

    def test_create_site_500(self):
        self.patch(site, 'create', fake_func)

        self.send_request(path = '/site', data = json.dumps({'name': 'test'}))
        self.assertEqual(falcon.HTTP_500, self.mock.status)

