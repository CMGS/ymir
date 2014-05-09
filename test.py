#!/usr/bin/python
#coding:utf-8

import os
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
    from query.comment import local
    for k, v in local.iteritems():
        v.drop_table(fail_silently=True)

if __name__ == '__main__':
    try:
        logger = logging.getLogger('peewee')
        logger.setLevel(logging.INFO)
        setup()
        os.environ['NOSE_WITH_COVERAGE'] = '1'
        os.environ['NOSE_COVER_PACKAGE'] = os.path.dirname(__file__)
        nose.main()
    except Exception:
        raise
    finally:
        cleanup()

