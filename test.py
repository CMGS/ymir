#!/usr/bin/python
#coding:utf-8

import os
import sys
import nose
import logging

global site

def setup():
    import tests
    import config
    for k in dir(config):
        value = getattr(tests, k, None)
        if not value:
            continue
        setattr(config, k, value)

    from models.site import Site, Block
    from query.site import create
    Site.create_table(fail_silently=True)
    Block.create_table(fail_silently=True)
    global site
    from tests.base import TEST_TOKEN
    site = create(TEST_TOKEN, 'test')

def cleanup():
    from models.site import Site, Block
    Site.drop_table(fail_silently=True)
    Block.drop_table(fail_silently=True)
    from utils.cache import local_cache
    for k, v in local_cache.iteritems():
        if not v:
            continue
        v.drop_table(fail_silently=True)
    from utils.cache import rds
    keys = rds.keys('c:*')
    if keys:
        rds.delete(*keys)

def generate_path():
    block = ['init', 'test', 'libs']
    path = os.path.realpath(os.path.dirname(__file__))
    for path in os.listdir(path):
        if not path.startswith('.') \
            and not path.startswith('__') \
            and (os.path.isdir(path) or path.endswith('py')):

            if path.endswith('py'):
                path = path.split('.py')[0]
            if path in block:
                continue
            yield path

if __name__ == '__main__':
    try:
        logger = logging.getLogger('peewee')
        logger.setLevel(logging.INFO)
        setup()
        sys.argv.append('--with-coverage')
        sys.argv.extend(['--cover-package=%s' % path for path in generate_path()])
        nose.main()
    except Exception:
        raise
    finally:
        cleanup()

