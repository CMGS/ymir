#!/usr/bin/python
#coding:utf-8

import json
import falcon

from query.site import block, get_site_by_token

from tests.base import is_iter
from tests.base import CommentTestBase

class TestBlock(CommentTestBase):

    def setUp(self):
        super(TestBlock, self).setUp()
        self.path = '/block'

    def test_add_block(self):
        site = get_site_by_token(self.token)
        after = site.blocks + 1
        response = self.send_request(
            path=self.path, method='PUT', \
            data=json.dumps({'ip': '192.168.1.1', 'token': self.token}), \
        )

        site = get_site_by_token(self.token)
        self.assertTrue(site.blocks, after)
        self.assertTrue(is_iter(response))
        self.assertEqual(falcon.HTTP_201, self.mock.status)
        data = json.loads(''.join(response))
        self.assertIsInstance(data, dict)
        id = data.get('id')
        self.assertTrue(id)
        self.assertIsInstance(id, int)

        self._test_bad_request(self.path, 'PUT')

    def test_rm_block(self):
        site = get_site_by_token(self.token)
        after = site.blocks
        nblock = block(site, '192.168.1.1')

        response = self.send_request(
            path=self.path, method='DELETE', \
            data=json.dumps({'id': nblock.id, 'token': self.token}), \
        )

        site = get_site_by_token(self.token)
        self.assertEqual(after, site.blocks)
        self.assertEqual(falcon.HTTP_200, self.mock.status)
        self.assertFalse(response)

    def test_get_block(self):
        response = self.send_request(
            path=self.path, method='GET', \
            data=json.dumps({'page': 1, 'token': self.token, 'num': 1}), \
        )

        self.assertTrue(is_iter(response))
        self.assertEqual(falcon.HTTP_200, self.mock.status)
        data = json.loads(''.join(response))
        self.assertIsInstance(data, list)

        self._test_bad_request('/block', 'GET', {'page': -1, 'token': self.token, 'num': 1})

