Getting Started
===============

What is ``awe`` for?
--------------------

``awe`` use cases:

* Create a report for some data you collected in your scripts.
* Poll some data in your script and update a chart with it.
* A replacement for print statements in your scripts that can include
   interactive tables, charts, headers, colors, etc... with minimum fuss.

``awe`` isn't for you if you need to:

* Handle large amounts of data. ``awe`` is quite wasteful in terms of resources. This works
  well for small-ish amounts of data. On the other hand, charts with many points will
  probably make your browser completely unresponsive.

Under the hood, ``awe`` generates the page using `React <https://github.com/facebook/react>`_.

Installation
------------

.. code-block:: sh

    pip install awe

Supported Python Versions
~~~~~~~~~~~~~~~~~~~~~~~~~

Tested on Python 2.7.15 and 3.7.1

Should work on many earlier versions I suppose, but haven't been tested so you can't be sure.

These days, I'm mostly working with Python 2.7, so things may unintentionally break on Python 3.
That being said, the test suite runs on both versions, so chances of that happening are not very high.

Support for Python 3 has been added after initial development, so please open an issue if something
seems broken under Python 3. In fact, open an issue if something seems broken under any Python version :)


Usage
-----

Begin by creating an ``awe.Page()`` instance. e.g:

.. code-block:: python

    from awe import Page
    page = Page()

A page is built by creating a hierarchy of elements.

Every element, including the root ``Page`` element, exposes ``new_XXX()`` methods that create element children.

These methods can create leaf elements such as ``new_text()``, ``new_table()``, etc... e.g:

.. code-block:: python

    page.new_text('Hello there')

They can also create container elements such as ``new_tabs()``, ``new_card()`` etc... e.g:

.. code-block:: python

    card = page.new_card()

If you don't intend to dynamically add data to an element, you can simply call the ``new_XXX()`` method with appropriate
arguments and be done with it.

If you do plan on adding data dynamically or create some element hierarchy, then keep a reference to the created
element, returned by the ``new_XXX()`` call. e.g:

.. code-block:: python

    card = page.new_card()
    text = card.new_text('Text inside of card')
    button = card.new_button(lambda: None)

The above creates a card as a child element of ``page`` and ``text`` and ``button`` elements as children of ``card``.

Once you're done with the initial page setup, call ``page.start()``. e.g:

.. code-block:: python

    # The default call will open a browser page without blocking the script
    page.start()

    # This will block the script
    page.start(block=True)

    # This will prevent the default browser open behavior
    page.start(open_browser=False)

Examples
--------

You can find many different examples of ``awe`` usage
`here <https://s3.amazonaws.com/awe-static-files/examples/awe_examples.html>`_.
