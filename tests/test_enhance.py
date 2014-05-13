#!/usr/bin/python
#coding:utf-8

import json
import falcon

from query.comment import create
from query.site import get_site_by_token

from tests.base import is_iter
from tests.base import TestBase

class TestEnhance(TestBase):

    def setUp(self):
        super(TestEnhance, self).setUp()

    def test_get_comments_by_ip(self):
        site = get_site_by_token(self.token)
        ip = '192.168.100.1'
        create(site, 20, 0, 1, ip, 'hello')
        create(site, 21, 0, 2, ip, 'world')

        data = {'ip': ip}
        response = self.send_request(
            path = '/mp/%s' % self.token, method = 'GET', \
            data = json.dumps(data), \
        )

        self.check(response)

    def test_get_comments_by_fid(self):
        site = get_site_by_token(self.token)
        ip = '192.168.101.1'
        f_comment = create(site, 30, 0, 1, ip, 'father')
        create(site, 30, f_comment.id, 1, ip, 'hello')
        create(site, 30, f_comment.id, 2, ip, 'world')

        data = {'tid': 30, 'fid': f_comment.id, 'page':1, 'num':2}
        response = self.send_request(
            path = '/mf/%s' % self.token, method = 'GET', \
            data = json.dumps(data), \
        )

        self.check(response)

    def check(self, response):
        self.assertTrue(is_iter(response))
        self.assertEqual(falcon.HTTP_200, self.mock.status)
        result = json.loads(''.join(response))
        self.assertTrue(result)
        self.assertIsInstance(result, list)

        rcomment_1, rcomment_2 = result
        self.assertTrue(rcomment_1['content'], 'hello')
        self.assertTrue(rcomment_2['content'], 'world')

