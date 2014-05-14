#!/usr/bin/python
#coding:utf-8

import json
import falcon

from query.comment import create, get_comment
from query.site import get_site_by_token

from tests.base import TestBase
from tests.base import fake_func

class TestEnhanceDelete(TestBase):

    def setUp(self):
        super(TestEnhanceDelete, self).setUp()
        self.delete_by_ip_path = '/dp/%s' % self.token
        self.create_path = '/m/%s' % self.token

    def test_delete_comment_by_ip(self):
        site = get_site_by_token(self.token)
        fc = create(site, 21, 0, 1, '127.0.0.1', 'hello')
        create(site, 21, fc.id, 1, '127.0.0.2', 'world')

        fc2 = create(site, 22, 0, 1, '127.0.0.3', 'hi')
        create(site, 22, fc2.id, 2, '127.0.0.4', 'man')
        create(site, 22, fc2.id, 3, '127.0.0.3', 'yo')

        create(site, 23, 0, 1, '127.0.0.3', 'hi')

        data = {'ip': '127.0.0.2'}
        response = self.send_request(
            path = self.delete_by_ip_path, method = 'DELETE', \
            data = json.dumps(data), \
        )

        self.assertEqual(falcon.HTTP_200, self.mock.status)
        self.assertFalse(response)
        fc_update = get_comment(site.id, site.token, site.node, fc.id)
        site_update = get_site_by_token(self.token)
        self.assertEqual(site.comments - 1, site_update.comments)
        self.assertEqual(fc_update.count, 0)

        data = {'ip': '127.0.0.3', 'tid': 23}
        response = self.send_request(
            path = self.delete_by_ip_path, method = 'DELETE', \
            data = json.dumps(data), \
        )

        self.assertEqual(falcon.HTTP_200, self.mock.status)
        self.assertFalse(response)
        fc2_update = get_comment(site.id, site.token, site.node, fc2.id)
        self.assertTrue(fc2_update)

        site = get_site_by_token(self.token)
        data = {'ip': '127.0.0.3'}
        response = self.send_request(
            path = self.delete_by_ip_path, method = 'DELETE', \
            data = json.dumps(data), \
        )
        self.assertEqual(falcon.HTTP_200, self.mock.status)
        self.assertFalse(response)
        site_update = get_site_by_token(self.token)
        self.assertEqual(site.comments - 3, site_update.comments)

    def test_delete_comment_by_ip_400(self):
        self._test_bad_request(self.delete_by_ip_path, 'DELETE')

    def test_delete_comment_by_ip_500(self):
        site = get_site_by_token(self.token)
        create(site, 24, 0, 1, '127.0.0.5', 'hello')
        from handlers import enhance
        self.patch(enhance, 'delete_comment', fake_func)

        self.send_request(
            path = self.delete_by_ip_path, \
            data = json.dumps({'ip': '127.0.0.5'}), \
            method = 'DELETE'
        )
        self.assertEqual(falcon.HTTP_500, self.mock.status)

