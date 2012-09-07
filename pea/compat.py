import sys


is_py3k = (sys.version_info >= (3, 0, 0))

if is_py3k:
    import unittest
else:
    import unittest2 as unittest
