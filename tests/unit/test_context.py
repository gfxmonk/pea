from mock import MagicMock, patch
import unittest2 as unittest

from pea.context import World, StepCollectionWrapper, step


####
##
## World._world
##
####

class DescribeWorldNoOp(unittest.TestCase):

    def should_always_return_false(self):
        self.assertFalse(World()._world())



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

class _BaseGetAttributeTest(unittest.TestCase):

    def setUp(self):
        self.world = World()
        self.expected = {'a': 1, 'b': 2}
        self.world._collection = self.expected
        self.configure()
        self.execute()

    def execute(self):
        try:
            self.returned = getattr(self.world, self.arg)
        except AttributeError as exc:
            self.exception = exc


class WhenGettingAnElementWithingTheWorldsCollection(_BaseGetAttributeTest):

    def configure(self):
        self.arg = 'a'

    def should_return_the_correct_value(self):
        self.assertEqual(self.returned, self.expected['a'])


class WhenGettingAnElementNotWithinTheWorldsCollection(_BaseGetAttributeTest):

    def configure(self):
        self.arg = 'z'

    def should_raise_an_attribute_error(self):
        self.assertIsInstance(self.exception, AttributeError)


####
##
## World.__setattr__
##
####

class _BaseSetAttributeTest(unittest.TestCase):

    def setUp(self):
        self.world = World()

        self.some_value = 'some_value'

        self.configure()
        self.execute()

    def execute(self):
        setattr(self.world, self.argument, self.some_value)


class WhenSettingAnAttriuteWithoutLeadingUnderscore(_BaseSetAttributeTest):

    def configure(self):
        self.argument = 'foobar'

    def should_insert_key_into_collection_dictionary(self):
        self.assertIn('foobar', self.world._collection)

    def should_insert_value_into_collection_dictionary(self):
        self.assertEqual(self.world._collection['foobar'], self.some_value)


class WhenSettingAnAttributeWithALeadingUnderscore(_BaseSetAttributeTest):

    def configure(self):
        self.argument = '_foobar'

    def should_not_be_inserted_into_collection_dictionary(self):
        self.assertNotIn('_foobar', self.world._collection)


####
##
## StepCollectionWrapper.__getattr__
##
####

class _BaseStepCollectionGetAttributeTest(unittest.TestCase):

    def setUp(self):
        self.prefix = 'Test'
        self.wrapper = StepCollectionWrapper(self.prefix)
        self.expected = {'test': lambda arg: arg}
        StepCollectionWrapper.steps = self.expected

        self.configure()
        self.execute()

    def execute(self):
        try:
            self.returned = getattr(self.wrapper, self.argument)
        except RuntimeError as exc:
            self.exception = exc


class WhenGettingAnAttributeWithinTheStepDict(_BaseStepCollectionGetAttributeTest):

    def configure(self):
        self.argument = 'test'

    def should_get_step_function_from_step_collection(self):
        self.assertEqual(
            StepCollectionWrapper.steps[self.argument],
            self.expected[self.argument],
        )

    def should_return_step_function_return_value(self):
        self.assertEqual(
            self.returned,
            self.expected[self.argument](self.prefix),
        )


class WhenGettingAnAttributeThatIsNotInStepsDict(_BaseStepCollectionGetAttributeTest):

    def configure(self):
        self.argument = 'failure'

    def should_raise_a_runtime_error(self):
        self.assertIsInstance(self.exception, RuntimeError)


####
##
## step
##
####

class _BaseStepFunctionStep(unittest.TestCase):

    @patch('pea.context.StepCollectionWrapper')
    @patch('pea.context.PeaFormatter')
    def setUp(self, formatter, wrapper):
        self.formatter = formatter
        self.wrapper = wrapper

        self.wrapper.steps = {}

        self.prefix = 'When'
        self.exception = None

        self.function = MagicMock()
        self.function.__name__ = 'MagicMock'

        self.configure()
        self.execute()

    def execute(self):
        try:
            self.returned = step(self.function)
        except RuntimeError as exc:
            self.exception = exc


class WhenFunctionNameIsNotAlreadyDefined(_BaseStepFunctionStep):

    def configure(self):
        pass

    def should_not_raise_runtime_error(self):
        self.assertIsNone(self.exception)

    def should_insert_function_name_into_step_collection(self):
        self.assertIn(self.function.__name__, self.wrapper.steps)


class WhenFunctionNameIsAlreadyDefined(_BaseStepFunctionStep):

    def configure(self):
        self.wrapper.steps = {self.function.__name__: 'boom goes the dynamite'}

    def should_raise_runtime_error(self):
        self.assertIsInstance(self.exception, RuntimeError)
