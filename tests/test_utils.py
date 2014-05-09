#!/usr/bin/python
#coding:utf-8

import json
from testtools import TestCase
from utils import fn
from utils import ijson

class TestFn(TestCase):

    def setUp(self):
        super(TestFn, self).setUp()
        self.mod = fn.dbs_mod
        self.len = fn.dbs_len

    def tearDown(self):
        super(TestFn, self).tearDown()
        fn.dbs_mod = self.mod
        fn.dbs_len = self.len

    def test_get_node(self):
        fn.dbs_mod = 10
        fn.dbs_len = 1
        assert fn.get_node(1) == 0
        assert fn.get_node(2) == 0
        fn.dbs_mod = 10
        fn.dbs_len = 2
        assert fn.get_node(1) == 1
        assert fn.get_node(4) == 0

class TestIjson(TestCase):

    def test_dump(self):
        cases = [
            {'a': 1, 'b': [1, 2, 3]}, \
            {'a': 1, 'b': 2}, \
            [1, 2, 3, 4, 5], \
            [1, 2, 'a', {'b': 'x'}], \
        ]
        for case in cases:
            self.compare(case)

    def compare(self, a):
        assert ''.join(ijson.dump(a)) == json.dumps(a)

