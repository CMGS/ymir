#!/usr/bin/python
#coding:utf-8

import json
import falcon
from falcon import testing

from app import app
from tests.base import is_iter
from tests.base import CommentTestBase

class TestSite(CommentTestBase):

    def setUp(self):
        super(TestSite, self).setUp()
        self.mock = testing.StartResponseMock()

    def test_add_site(self):
        response = app(
            testing.create_environ(
                path='/site', \
                method='PUT', \
                body=json.dumps({'name': 'test'}), \
            ), \
            self.mock, \
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

