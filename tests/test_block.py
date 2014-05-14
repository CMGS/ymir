#!/usr/bin/python
#coding:utf-8

import json
import falcon

from query.site import block, get_site_by_token

from tests.base import is_iter
from tests.base import TestBase
from tests.base import fake_func

class TestBlock(TestBase):

    def setUp(self):
        super(TestBlock, self).setUp()
        self.path = '/block'

    def test_create_block(self):
        site = get_site_by_token(self.token)
        after = site.blocks + 1
        response = self.send_request(
            path = self.path, method = 'PUT', \
            data = json.dumps({'ip': '192.168.1.1', 'token': self.token}), \
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

    def test_create_block_400(self):
        self._test_bad_request(self.path, 'PUT')

    def test_create_block_500(self):
        from handlers import site
        self.patch(site, 'block', fake_func)

        self.send_request(
            path = self.path, method = 'PUT', \
            data = json.dumps({'ip': '192.168.1.1', 'token': self.token}), \
        )
        self.assertEqual(falcon.HTTP_500, self.mock.status)

    def test_delete_block(self):
        site = get_site_by_token(self.token)
        after = site.blocks
        nblock = block(site, '192.168.1.1')

        response = self.send_request(
            path = self.path, method = 'DELETE', \
            data = json.dumps({'id': nblock.id, 'token': self.token}), \
        )

        site = get_site_by_token(self.token)
        self.assertEqual(after, site.blocks)
        self.assertEqual(falcon.HTTP_200, self.mock.status)
        self.assertFalse(response)

    def test_delete_block_500(self):
        site = get_site_by_token(self.token)
        nblock = block(site, '192.168.1.1')
        from handlers import site
        self.patch(site, 'delete_block', fake_func)

        self.send_request(
            path = self.path, method = 'DELETE', \
            data = json.dumps({'id': nblock.id, 'token': self.token}), \
        )
        self.assertEqual(falcon.HTTP_500, self.mock.status)

    def test_get_block(self):
        response = self.send_request(
            path = self.path, method='GET', \
            data = json.dumps({'page': 1, 'token': self.token, 'num': 1}), \
        )

        self.assertTrue(is_iter(response))
        self.assertEqual(falcon.HTTP_200, self.mock.status)
        data = json.loads(''.join(response))
        self.assertIsInstance(data, list)

    def test_get_block_400(self):
        data = {'page': -1, 'token': self.token, 'num': 1}
        self._test_bad_request(self.path, 'GET', data = data)
        self._test_bad_request(self.path, 'GET', {'page': -1, 'num': 1})

