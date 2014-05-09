#!/usr/bin/python
#coding:utf-8

import nose

def setup():
    import tests
    import config
    for k in dir(config):
        value = getattr(tests, k, None)
        if not value:
            continue
        setattr(config, k, value)

    from models.site import Site, Block
    Site.create_table(fail_silently=True)
    Block.create_table(fail_silently=True)

def cleanup():
    from models.site import Site, Block
    Site.drop_table(fail_silently=True)
    Block.drop_table(fail_silently=True)
    from query.comment import local
    for k, v in local.iteritems():
        v.drop_table(fail_silently=True)

if __name__ == '__main__':
    try:
        setup()
        nose.main()
    except Exception:
        raise
    finally:
        cleanup()

