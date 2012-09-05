from mock import patch, Mock
import unittest2 as unittest

from pea import formatter


####
##
## describe
##
####

class _BaseDescriptionTest(unittest.TestCase):

    @patch('pea.formatter.termstyle')
    @patch('pea.formatter._render')
    def setUp(self, render, termstyle):
        self.render = render
        self.termstyle = termstyle

        self.prefix = 'When'
        self.name = 'test'
        self.color = Mock()

        self.configure()
        self.execute()

    def execute(self):
        self.returned = formatter.describe(
            self.prefix,
            self.name,
            self.color,
            *self.args,
            **self.kwargs
        )


class WhenDescribingArgs(_BaseDescriptionTest):

    def configure(self):
        self.args = [Mock(), Mock()]
        self.kwargs = {}
        self.render.return_value = 'foo'
        self.termstyle.bold.return_value = 'bar'

    def should_embolden_the_string_representation_of_the_args(self):
        self.termstyle.bold.assert_called_once_with('foo foo')

    def should_apply_termstyle_coloring_to_bold_string(self):
        expected = ('\t{0} {1}: {2}'
            .format(self.prefix, self.name, self.termstyle.bold.return_value)
        )
        self.color.assert_called_once_with(expected)

    def should_return_termstyle_rendering_to_bold_string(self):
        self.assertEqual(self.returned, self.color.return_value)


class WhenDescribingKwargs(_BaseDescriptionTest):

    def configure(self):
        self.kwargs = {'mock1': Mock(), 'mock2': Mock()}
        self.args = []
        self.render.return_value = 'foo'
        self.termstyle.bold.return_value = 'bar=baz'

    def should_render_the_kwargs(self):
        self.render.assert_any_call(self.kwargs['mock1'])
        self.render.assert_any_call(self.kwargs['mock2'])

    def should_embolden_the_string_representation_of_the_kwargs(self):
        self.termstyle.bold.assert_called_once_with('mock2=foo, mock1=foo')

    def should_apply_termstyle_coloring_to_bold_string(self):
        expected = ('\t{0} {1}: {2}'
            .format(self.prefix, self.name, self.termstyle.bold.return_value)
        )
        self.color.assert_called_once_with(expected)

    def should_return_termstyle_rendering_to_bold_string(self):
        self.assertEqual(self.returned, self.color.return_value)


class WhenDesribingNeitherArgsOrKwargs(_BaseDescriptionTest):

    def configure(self):
        self.kwargs = {}
        self.args = []

    def should_apply_termstyle_rendering_of_prefix_and_name(self):
        expected = '\t{0} {1}'.format(self.prefix, self.name)
        self.color.assert_called_once_with(expected)

    def should_return_termstyle_rendering_of_string(self):
        self.assertEqual(self.returned, self.color.return_value)


####
##
## _render
##
####

class _BaseRender(unittest.TestCase):

    @patch('pea.formatter._render_dict')
    def setUp(self, render_dict):
        self.render_dict = render_dict
        self.configure()
        self.execute()

    def execute(self):
        self.returned = formatter._render(self.arg)


class WhenRenderingADictionary(_BaseRender):

    def configure(self):
        self.arg = {}

    def should_call_render_dict_if_the_arg_is_a_dict(self):
        self.render_dict.assert_called_once_with(self.arg)


class WhenNotRenderingADictonary(_BaseRender):

    def configure(self):
        self.arg = 'abc'

    def should_return_unicode(self):
        self.assertIsInstance(self.returned, unicode)



####
##
## _render_dict
##
####

class DescribeRenderDict(unittest.TestCase):

    def setUp(self):
        self.kwargs = {'a': 1, 'b': 2}

        self.execute()

    def execute(self):
        self.returned = formatter._render_dict(self.kwargs)

    def should_return_formatted_string(self):
        expected = ', '.join(
            '{0}: <{1}>'.format(k, self.kwargs[k].__class__.__name__)
            for k in self.kwargs
        )

        self.assertEqual(
            self.returned,
            '{' + expected + '}'
        )
