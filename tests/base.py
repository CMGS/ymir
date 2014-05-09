#!/usr/bin/python
#coding:utf-8

import types
import fixtures
from falcon import testing

def is_iter(o):
    return isinstance(o, types.GeneratorType)

class CommentFixture(fixtures.Fixture):
    def setUp(self):
        super(CommentFixture, self).setUp()
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

    def tearDown(self):
        from models.site import Site, Block
        Site.drop_table(fail_silently=True)
        Block.drop_table(fail_silently=True)
        import common
        common.default_db.execute_sql('DROP TABLE IF EXISTS `comment_1;`')

server = CommentFixture()

class CommentTestBase(testing.TestBase):

    def setUp(self):
        super(CommentTestBase, self).setUp()
        self.useFixture(server)

    def tearDown(self):
        super(CommentTestBase, self).tearDown()
        server.tearDown()

