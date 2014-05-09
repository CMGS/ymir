#!/usr/bin/python
#coding:utf-8

import falcon
from falcon import testing

from app import app
from tests.base import CommentTestBase

class TestApp(CommentTestBase):

    def test_app(self):
        mock = testing.StartResponseMock()
        response = app(testing.create_environ(), mock)

        self.assertEqual(falcon.HTTP_200, mock.status)
        self.assertIsInstance(response, list)
        self.assertEqual(response[0], 'Hello World')

