#!/usr/bin/python
#coding:utf-8

import json
import config
import falcon
from falcon import testing

from app import app
from tests.base import is_iter
from tests.base import CommentTestBase

class TestSys(CommentTestBase):

    def test_get(self):
        response = app(testing.create_environ(path='/sys'), self.mock)

        self.assertTrue(is_iter(response))
        self.assertEqual(falcon.HTTP_200, self.mock.status)

        data = json.loads(''.join(response))
        self.assertIsInstance(data, dict)
        self.assertEqual(data['store'], config.STORE)

