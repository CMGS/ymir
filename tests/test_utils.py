#!/usr/bin/python
#coding:utf-8

import json
from testtools import TestCase
from utils import fn
from utils import ijson

class TestFn(TestCase):

    def test_get_node(self):
        self.patch(fn, 'dbs_mod', 10)
        self.patch(fn, 'dbs_len', 1)
        self.assertEqual(fn.get_node(1), 0)
        self.assertEqual(fn.get_node(2), 0)
        self.patch(fn, 'dbs_mod', 10)
        self.patch(fn, 'dbs_len', 9)
        self.assertEqual(fn.get_node(77), 7)
        self.assertEqual(fn.get_node(23), 3)

class TestIjson(TestCase):

    def test_dump(self):
        cases = [
            {'a': 1, 'b': [1, 2, 3]}, \
            {'a': 1, 'b': 2}, \
            [1, 2, 3, 4, 5], \
            [1, 2, 'a', {'b': 'x'}], \
            {u'123': u'bbbb' }, \
        ]
        for case in cases:
            self.compare(case)

    def compare(self, a):
        self.assertEqual(''.join(ijson.dump(a)), json.dumps(a))

