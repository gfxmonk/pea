from compat import unittest

from pea.formatter import PeaFormatter

__all__ = (
    'world',
    'step',
    'TestCase',
    'Given',
    'When',
    'Then',
    'And',
)


class World(unittest.TestCase):

    def __init__(self):
        self._reset()
        super(World, self).__init__('_world')

    def _world(self):
        # Unittest2 Test case requires this method so we have it no-op
        return False

    def _reset(self):
        self._collection = {}

    def __getattr__(self, val):
        if val in self._collection:
            return self._collection[val]
        else:
            raise AttributeError(
                'The variable {0} was not located in the world object'
                .format(val),
            )

    def __setattr__(self, attr, val):
        if attr.startswith('_'):
            super(World, self).__setattr__(attr, val)
        else:
            self._collection[attr] = val


class StepCollectionWrapper(object):

    steps = {}

    def __init__(self, prefix):
        self._prefix = prefix

    def __getattr__(self, value):
        if value not in StepCollectionWrapper.steps:
            raise RuntimeError(
                'Step function "{0}" was not defined'
                .format(value)
            )

        attr = StepCollectionWrapper.steps[value]
        return attr(self._prefix)


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global world
        world = World()
        StepCollectionWrapper.steps = {}


world = World()

Given = StepCollectionWrapper('Given')
When = StepCollectionWrapper('When')
Then = StepCollectionWrapper('Then')
And = StepCollectionWrapper('And')


def step(func):
    function_name = func.__name__

    if function_name in StepCollectionWrapper.steps:
        raise RuntimeError(
            'The step function "{0}" was already defined in the module "{1}"'
            .format(func.__name__, func.__module__),
        )

    function_closure = lambda prefix: PeaFormatter.with_formatting(prefix, func)
    StepCollectionWrapper.steps[function_name] = function_closure

    return func
