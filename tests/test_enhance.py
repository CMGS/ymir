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
        self.get_comments_by_ip_path = '/mp/%s' % self.token
        self.get_comments_by_fid_path = '/mf/%s' % self.token

    def test_get_comments_by_ip(self):
        site = get_site_by_token(self.token)
        ip = '192.168.100.1'
        create(site, 20, 0, 1, ip, 'hello')
        create(site, 21, 0, 2, ip, 'world')

        data = {'ip': ip}
        response = self.send_request(
            path = self.get_comments_by_ip_path, method = 'GET', \
            data = json.dumps(data), \
        )
        self.check(response)

        data = {'ip': ip, 'tid': 20}
        response = self.send_request(
            path = self.get_comments_by_ip_path, method = 'GET', \
            data = json.dumps(data), \
        )
        self.check(response)

    def test_get_comments_by_ip_400(self):
        self._test_bad_request(self.get_comments_by_ip_path, 'GET')

    def test_get_comments_by_fid(self):
        site = get_site_by_token(self.token)
        ip = '192.168.101.1'
        f_comment = create(site, 30, 0, 1, ip, 'father')
        create(site, 30, f_comment.id, 1, ip, 'hello')
        create(site, 30, f_comment.id, 2, ip, 'world')

        data = {'tid': 30, 'fid': f_comment.id, 'page':1, 'num':2}
        response = self.send_request(
            path = self.get_comments_by_fid_path, method = 'GET', \
            data = json.dumps(data), \
        )

        self.check(response)

        data = {'tid': 30, 'fid': f_comment.id, 'page':1, 'num':2}
        response = self.send_request(
            path = self.get_comments_by_fid_path, method = 'GET', \
            data = json.dumps(data), \
        )

        self.check(response)

    def test_get_comments_by_fid_400(self):
        data = {'tid': 30, 'page':1, 'num':2}
        self.send_request(
            path = self.get_comments_by_fid_path, method = 'GET', \
            data = json.dumps(data), \
        )
        self.assertEqual(falcon.HTTP_400, self.mock.status)

    def test_get_comments_by_fid_404(self):
        data = {'tid': 30, 'fid': 10000, 'page':1, 'num':2}
        self.send_request(
            path = self.get_comments_by_fid_path, method = 'GET', \
            data = json.dumps(data), \
        )
        self.assertEqual(falcon.HTTP_404, self.mock.status)

        data = {'tid': 30, 'fid': 10000, 'page':1, 'num':2}
        self.send_request(
            path = self.get_comments_by_fid_path, method = 'GET', \
            data = json.dumps(data), \
        )
        self.assertEqual(falcon.HTTP_404, self.mock.status)

    def check(self, response):
        self.assertTrue(is_iter(response))
        self.assertEqual(falcon.HTTP_200, self.mock.status)
        result = json.loads(''.join(response))
        self.assertTrue(result)
        self.assertIsInstance(result, list)

        self.check_comment(result)

    def check_comment(self, result):
        if len(result) == 2:
            rcomment_1, rcomment_2 = result
            self.assertTrue(rcomment_1['content'], 'hello')
            self.assertTrue(rcomment_2['content'], 'world')
            return

        self.assertTrue(result[0]['content'], 'hello')

