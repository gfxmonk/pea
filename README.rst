pea - The tiniest green vegetable.
-------------------------------------

**pea** is a minimal BDD framework for python, in the style of ruby's `cucumber`_ and
python's `lettuce`_. It aims to help you write the same kind of tests - but in straight-up
python code, without all the parsing and indirection and other hoops to jump through. It's
a lot like ruby's `coulda`_.

Benefits of cucumber-style testing include:

- You write your tests in clear, english language without inline code
- Your tests are human-readable, and hopefully human-editable
- You can re-use steps with confidence, because they all do exactly what
  they say on the tin

Benefits of ``pea`` over ``lettuce``, ``cucumber``, etc:

- It's a really trivial library (thus the name). It doesn't do very much,
  so it probably doesn't have many bugs

- Your features are just python code:

  - No "BDD language parser" needed
  - No regular expressions
  - Stack traces make sense
  - Syntax highlighting
  - You can use `ctags`_ to jump between test & implementation, as well as
    for method completion
  - Managing and renaming functions is much easier than managing regexes
  - You can use whatever abstractions you like
  - You can use rich python objects as arguments, instead of parsing strings

- It doesn't need its own test runner; so you can just use `nose`_ to run it
  alongside your unit tests


So how do I use it?
--------------------------------------

Here's a minimal example:

.. code:: python

	from pea import *

	@step
	def I_go_to_the_store():
		world.location='store'
		world.cart = []

	@step
	def I_buy_some(item):
		world.cart.append(item)

	@step
	def I_go_home():
		world.location = 'home'

	@step
	def I_have_some_delicious(item):
		assert item in world.cart
		world.assertEquals(world.location, 'home')

	# --------------------

	class TestShopping(TestCase):
		def test_buying_some_peas(self):

			Given.I_go_to_the_store()
			When.I_buy_some('peas')
			And.I_go_home()
			Then.I_have_some_delicious('peas')

... and when you run it (with nosetests, in verbose mode):

.. image:: http://gfxmonk.net/dist/0install/pea/screenshot.png


Basics:
^^^^^^^

- ``@step`` adds your function to pea's registry of steps, which allows
  them to be called via ``Given``, ``When``, ``And``, and ``Then``.
- To re-use a step from inside another step, just call the function!

Stuff to remember:
^^^^^^^^^^^^^^^^^^
- Make sure you inherit from ``pea.TestCase`` (and call ``super`` from ``setUpClass``),
  as it takes care of resetting the ``world`` between tests.
- You can use ``TestCase`` assertion methods on the world, too
  - e.g. ``world.assertEquals(expected, actual)``
- You can only have one TestCase class in each module since it destroys
  the step collection after the tests have been completed.  If you would like
  to have more test classes on one module then create a base class that
  inherits from ``TestCase`` and have your tests inherit from that.

Pea works well with `rednose`_

.. _cucumber: http://cukes.info/
.. _coulda: https://github.com/elight/coulda
.. _lettuce: https://github.com/gabrielfalcao/lettuce/
.. _ctags: http://ctags.sourceforge.net/
.. _nose: http://somethingaboutorange.com/mrl/projects/nose/1.0.0/
.. _rednose: https://github.com/gfxmonk/rednose/tree
