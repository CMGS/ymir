#!/usr/bin/python
#coding:utf-8

import falcon
from tests.base import TestBase

class TestHeatProtect(TestBase):

    def test_get_app_overheat(self):
        headers = {'X-Real-IP':'192.168.1.1'}

        for i in xrange(0, 5):
            self.send_request(
                path = '/sys', method = 'GET', \
                headers = headers
            )

        self.assertEqual(falcon.HTTP_403, self.mock.status)

