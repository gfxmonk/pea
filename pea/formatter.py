from __future__ import unicode_literals, print_function

import nose
import functools
import termstyle


line_length = 77


class PeaFormatter(nose.plugins.Plugin):
    name = 'pea'
    score = 500
    instance = None
    new_test = False
    stream = None
    enabled = True

    def setOutputStream(self, stream):
        PeaFormatter.stream = stream

    def configure(self, options, conf):
        PeaFormatter.enabled = options.verbosity >= 2
        if not PeaFormatter.enabled:
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
        if PeaFormatter.enabled and not self.new_test:
            print('', file=self.stream)

    @classmethod
    def with_formatting(cls, prefix, func):

        @functools.wraps(func)
        def _run(*args, **kwargs):
            if not cls.enabled:
                return func(*args, **kwargs)

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
    """Assemble the output for the test case by applying style and colors"""
    if args:
        fmt_string = '\t{0} {1}: {2}'
        rendered_args = ' '.join(_render(arg) for arg in args)
        args = termstyle.bold(rendered_args)
        string = fmt_string.format(prefix, name, args)
        return color(string)
    elif kwargs:
        fmt_string = '{0}={1}'
        rendered_kargs = [
            fmt_string.format(key, _render(kwargs[key])) for key in kwargs
        ]
        kwargs = termstyle.bold(', ' .join(rendered_kargs))
        return color('\t' + '{0} {1}: {2}'.format(prefix, name, kwargs))
    else:
        return color('\t{0} {1}'.format(prefix, name))


def _render(arg):
    """Will return a unicode representation of the argument if it is not a dict
    otherwise it will render the dictionary differently

    """
    if _is_dict(arg):
        return _render_dict(arg)
    else:
        return unicode(arg)


def _is_dict(arg):
    return isinstance(arg, dict)


def _render_dict(kwargs):
    """Provides an abridged look at a dictionary structure so the
    argument display for the test dosen't span many lines and look cluttered.
    It will only show the keys and the types of ther values for the first
    level of the dictionary.  Nested dictionary structures will simply appear
    like {key: <dict>}

    The dictionary representation will look something like the following:

    {key1: <type of key1s value>, key2: <type of key2s value>, ...}

    """
    fmt_string = "{0}: <{1}>"
    args = [fmt_string.format(key, kwargs[key].__class__.__name__) for key in kwargs]
    return '{' + ', '.join(args) + '}'
