from __future__ import unicode_literals, print_function

import nose
import functools
import termstyle

failure = 'FAILED'
error = 'ERROR'
success = 'passed'
skip = 'skipped'
line_length = 77


class PeaFormatter(nose.plugins.Plugin):
    name = 'pea'
    score = 500
    instance = None
    new_test = False
    stream = None

    def __init__(self):
        self.enabled = False
        PeaFormatter.instance = self

    def setOutputStream(self, stream):
        PeaFormatter.stream = stream

    def configure(self, options, conf):
        self.enabled = options.verbosity >= 2
        if not self.enabled:
            return
        color = getattr(options, 'color', True)
        force_color = getattr(options, 'force_color', False)
        if color:
            try:
                (termstyle.enable if force_color else termstyle.auto)()
            except TypeError:  # happens when stdout is closed
                pass
        else:
            termstyle.disable()

    def beforeTest(self, test):
        PeaFormatter.new_test = True

    def afterTest(self, test):
        if self.enabled and not self.new_test:
            print('', file=self.stream)

    @classmethod
    def with_formatting(cls, prefix, func):

        @functools.wraps(func)
        def _run(*args, **kwargs):
            name = func.__name__.replace('_', ' ')
            color = termstyle.green
            try:
                return func(*args, **kwargs)
            except:
                color = termstyle.red
                raise
            finally:
                if PeaFormatter.new_test:
                    PeaFormatter.new_test = False
                    print('', file=cls.stream)

                output = describe(prefix, name, color, *args, **kwargs)
                print(output, file=cls.stream)

        return _run


def describe(prefix, name, color, *args, **kwargs):
    if args:
        fmt_string = '\t{0} {1} {2}'
        args = ' '.join(unicode(arg) for arg in args)
        string = fmt_string.format(prefix, name, args)
        return color(string)
    elif kwargs:
        fmt_string = '{0}={1}'
        strings = [fmt_string.format(key, kwargs[key]) for key in kwargs]
        kwargs = '{' + ', '.join(strings) + '}'
        return color('\t' + ' '.join((prefix, name, kwargs)))
    else:
        return color('\t{0} {1}'.format(prefix, name))
