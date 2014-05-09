#!/usr/bin/python
#coding:utf-8

import json
import falcon
from falcon import testing

from app import app

from tests.base import is_iter
from tests.base import TEST_TOKEN
from tests.base import CommentTestBase

class TestBlock(CommentTestBase):

    def setUp(self):
        super(TestBlock, self).setUp()
        self.mock = testing.StartResponseMock()

    def test_add_block(self):
        response = app(
            testing.create_environ(
                path='/block', \
                method='PUT', \
                body=json.dumps({'ip': '192.168.1.1', 'token': TEST_TOKEN}), \
            ), \
            self.mock, \
        )

        self.assertTrue(is_iter(response))
        self.assertEqual(falcon.HTTP_201, self.mock.status)
        data = json.loads(''.join(response))
        self.assertIsInstance(data, dict)
        id = data.get('id')
        self.assertTrue(id)
        self.assertIsInstance(id, int)

        self._test_bad_request('/block', 'PUT')


    def test_rm_block(self):
        from query.site import block, get_site_by_token

        site = get_site_by_token(TEST_TOKEN)
        block = block(site, '192.168.1.1')

        response = app(
            testing.create_environ(
                path='/block', \
                method='DELETE', \
                body=json.dumps({'id': block.id, 'token': TEST_TOKEN}), \
            ), \
            self.mock, \
        )

        self.assertEqual(falcon.HTTP_200, self.mock.status)

    def test_get_block(self):
        pass

