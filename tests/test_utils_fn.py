#!/usr/bin/python
#coding:utf-8

from utils import fn
from nose import with_setup

mod = 0
len = 0

def setup_func():
    global mod, len
    mod = fn.dbs_mod
    len = fn.dbs_len

def teardown_func():
    fn.dbs_mod = mod
    fn.dbs_len = len

@with_setup(setup_func, teardown_func)
def test_get_node():
    fn.dbs_mod = 10
    fn.dbs_len = 1
    assert fn.get_node(1) == 0
    assert fn.get_node(2) == 0
    fn.dbs_mod = 10
    fn.dbs_len = 2
    assert fn.get_node(1) == 1
    assert fn.get_node(4) == 0

