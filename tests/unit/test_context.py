import unittest2 as unittest

from pea.context import World


####
##
## World._reset
##
####


class WhenResettingTheWorldCollection(unittest.TestCase):

    def setUp(self):
        self.world = World()
        self.world._collection = {'a': 1, 'b': 2}
        self.execute()

    def execute(self):
        self.world._reset()

    def should_create_new_dictionary(self):
        self.assertEqual(self.world._collection, {})


####
##
## World.__getattr__
##
####

class WhenSettingAnAttribute(unittest.TestCase):

    def setUp(self):
        self.world = World()
        self.expected = {'a': 1, 'b': 2}
        self.world._collection = self.expected
        self.execute()

    def execute(self):
        self.returned = self.world.a

    def should_return_value_from_collection_dict(self):
        self.assertEqual(self.returned, self.expected['a'])


####
##
## World.__setattr__
##
####

class _BaseSetAttributeTest(unittest.TestCase):

    def setUp(self):
        self.world = World()

        self.configure()
        self.execute()


class WhenSettingAttriutesWithoutLeadingUnderscore(_BaseSetAttributeTest):

    def configure(self):
        self.argument = 'foobar'

    def execute(self):
        self.world.argument = self.argument

    def should_insert_key_into_collection_dictionary(self):
        self.assertIn('argument', self.world._collection)

    def should_insert_value_into_collection_dictionary(self):
        self.assertEqual(self.world._collection['argument'], self.argument)


