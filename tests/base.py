#!/usr/bin/python
#coding:utf-8

import json
import config
import types
from app import app
import falcon
from falcon import testing
from utils.fn import Obj

TEST_TOKEN = 'test_token'

def wrap(f):
    def _(*args, **kwargs):
        r = f(*args, **kwargs)
        for i in r:
            if isinstance(i, Obj):
                i.ctime = True
            yield i
    return _

def is_iter(o):
    return isinstance(o, types.GeneratorType)

def fake_func(*args, **kwargs):
    raise Exception('this is test')

class TestBase(testing.TestBase):

    def setUp(self):
        super(TestBase, self).setUp()
        self.mock = testing.StartResponseMock()
        self.token = TEST_TOKEN

    def tearDown(self):
        super(TestBase, self).tearDown()

    def _test_bad_request(self, path, method, data=None):
        response = self.send_request(path, json.dumps(data or {}), method)

        self.assertIsInstance(response, list)
        result = json.loads(response[0])
        self.assertEqual(result['title'], config.HTTP_400)
        self.assertEqual(falcon.HTTP_400, self.mock.status)

    def send_request(self, path='/', data='', method='PUT', **kwargs):
        response = app(
            testing.create_environ(
                path=path, \
                method=method, \
                body=data, \
                **kwargs
            ), \
            self.mock, \
        )
        return response

