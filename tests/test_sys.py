#!/usr/bin/python
#coding:utf-8

import json
import config
import falcon

from tests.base import is_iter
from tests.base import TestBase

class TestSys(TestBase):

    def test_get_sys_info(self):
        response = self.send_request(
                path='/sys', method='GET', \
        )

        self.assertTrue(is_iter(response))
        self.assertEqual(falcon.HTTP_200, self.mock.status)

        data = json.loads(''.join(response))
        self.assertIsInstance(data, dict)
        self.assertEqual(data['store'], config.STORE)

