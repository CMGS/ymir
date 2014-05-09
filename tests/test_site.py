#!/usr/bin/python
#coding:utf-8

import json
import config
import falcon
from falcon import testing

from app import app
from tests.base import is_iter
from tests.base import CommentTestBase

class TestSite(CommentTestBase):

    def test_add_site(self):
        mock = testing.StartResponseMock()
        response = app(
            testing.create_environ(
                path='/site', \
                method='PUT', \
                body=json.dumps({'name': 'test'}), \
            ), \
            mock, \
        )

        self.assertTrue(is_iter(response))
        self.assertEqual(falcon.HTTP_201, mock.status)
        data = json.loads(''.join(response))
        self.assertIsInstance(data, dict)
        token = data.get('token')
        self.assertTrue(token)
        self.assertIsInstance(token, (str, unicode))
        self.assertEqual(len(token), 32)

        response = app(
            testing.create_environ(
                path='/site', \
                method='PUT', \
                body=json.dumps({}), \
            ), \
            mock, \
        )

        self.assertIsInstance(response, list)
        result = json.loads(response[0])
        self.assertEqual(result['title'], config.HTTP_400)
        self.assertEqual(falcon.HTTP_400, mock.status)

