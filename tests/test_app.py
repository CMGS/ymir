#!/usr/bin/python
#coding:utf-8

import falcon
from tests.base import CommentTestBase

class TestApp(CommentTestBase):

    def test_app(self):
        response = self.send_request(method='GET')

        self.assertEqual(falcon.HTTP_200, self.mock.status)
        self.assertIsInstance(response, list)
        self.assertEqual(response[0], 'Hello World')

