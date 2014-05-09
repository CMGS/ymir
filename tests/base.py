#!/usr/bin/python
#coding:utf-8

import types
from falcon import testing

def is_iter(o):
    return isinstance(o, types.GeneratorType)

class CommentTestBase(testing.TestBase):

    def setUp(self):
        super(CommentTestBase, self).setUp()

    def tearDown(self):
        super(CommentTestBase, self).tearDown()

