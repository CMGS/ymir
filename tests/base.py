#!/usr/bin/python
#coding:utf-8

import json
import config
import types
from app import app
import falcon
from falcon import testing

TEST_TOKEN = 'test_token'

def is_iter(o):
    return isinstance(o, types.GeneratorType)

class CommentTestBase(testing.TestBase):

    def setUp(self):
        super(CommentTestBase, self).setUp()

    def tearDown(self):
        super(CommentTestBase, self).tearDown()

    def _test_bad_request(self, path, method, data=None):
        response = app(
            testing.create_environ(
                path=path, \
                method=method, \
                body=json.dumps(data or {}), \
            ), \
            self.mock, \
        )

        self.assertIsInstance(response, list)
        result = json.loads(response[0])
        self.assertEqual(result['title'], config.HTTP_400)
        self.assertEqual(falcon.HTTP_400, self.mock.status)


