#!/usr/bin/python
#coding:utf-8

import json
import falcon

from query.comment import create
from query.site import block, get_site_by_token

from tests.base import is_iter
from tests.base import CommentTestBase

class TestComment(CommentTestBase):

    def setUp(self):
        super(TestComment, self).setUp()
        self.path = '/m/%s' % self.token

    def test_add_comment(self):
        data = {'tid':1, 'fid':1, 'uid':1, 'ip':'192.168.8.1', 'content':'Hello World'}
        response = self.send_request(
            path=self.path, method='PUT', \
            data=json.dumps(data), \
        )

        self.assertTrue(is_iter(response))
        self.assertEqual(falcon.HTTP_201, self.mock.status)
        data = json.loads(''.join(response))
        self.assertIsInstance(data, dict)
        id = data.get('id')
        self.assertTrue(id)
        self.assertIsInstance(id, int)

        self._test_bad_request(self.path, 'PUT', {'tid':1, 'fid':1, 'uid':1, 'ip':'192.168.1.1',})

    def test_add_comment_deny(self):
        site = get_site_by_token(self.token)
        block(site, '192.168.9.1')
        data = {'tid':1, 'fid':1, 'uid':1, 'ip':'192.168.9.1', 'content':'Hello World'}
        response = self.send_request(
            path=self.path, method='PUT', \
            data=json.dumps(data), \
        )

        self.assertIsInstance(response, list)
        self.assertEqual(falcon.HTTP_403, self.mock.status)

    def test_get_empty(self):
        data = {'tid':100, 'page':1, 'num':1, 'expand':0}
        response = self.send_request(
            path=self.path, method='GET', \
            data=json.dumps(data), \
        )

        self.assertTrue(is_iter(response))
        self.assertEqual(falcon.HTTP_200, self.mock.status)
        self.assertFalse(json.loads(''.join(response)))

    def test_get_comment_no_expand(self):
        site = get_site_by_token(self.token)
        ncomment_1 = create(site, 10, 0, 1, '192.168.10.1', 'hello')

        data = {'tid':10, 'page':1, 'num':1, 'expand':0}
        response = self.send_request(
            path=self.path, method='GET', \
            data=json.dumps(data), \
        )

        self.assertTrue(is_iter(response))
        self.assertEqual(falcon.HTTP_200, self.mock.status)
        result = json.loads(''.join(response))
        self.assertTrue(result)

        data = result[0][0]
        self.assertEqual(data['ip'], ncomment_1.ip)
        self.assertEqual(data['content'], ncomment_1.content)
        self.assertEqual(data['id'], ncomment_1.id)

    def test_get_comment_with_expand(self):
        site = get_site_by_token(self.token)
        ncomment_1 = create(site, 11, 0, 1, '192.168.10.1', 'hello')
        ncomment_2 = create(site, 11, ncomment_1.id, 1, '192.168.10.1', 'world')

        data = {'tid':11, 'page':1, 'num':3, 'expand':1}
        response = self.send_request(
            path=self.path, method='GET', \
            data=json.dumps(data), \
        )

        self.assertTrue(is_iter(response))
        self.assertEqual(falcon.HTTP_200, self.mock.status)
        result = json.loads(''.join(response))
        self.assertTrue(result)

        c1, c2 = result[0]
        self.assertEqual(c1['ip'], ncomment_1.ip)
        self.assertEqual(c1['content'], ncomment_1.content)
        self.assertEqual(c1['id'], ncomment_1.id)

        self.assertEqual(c2['ip'], ncomment_2.ip)
        self.assertEqual(c2['content'], ncomment_2.content)
        self.assertEqual(c2['id'], ncomment_2.id)

