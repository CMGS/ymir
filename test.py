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
    import common
    common.default_db.execute_sql('DROP TABLE IF EXISTS `comment_1;`')

if __name__ == '__main__':
    try:
        setup()
        nose.main()
    except Exception:
        raise
    finally:
        cleanup()

