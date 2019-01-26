DSL
===

``awe``'s DSL lets you create element hierarchies using markup similar to HTML and inspired by react.

The markup though, is built from basic data structures (lists and dicts) and is not similar to HTML in that regard.

Everything that can be created with the ``DSL``, can be created using ``awe`` API directly.

This page will go over the different DSL features and show how they compare to using the API directly.

.. note::
    The examples shown below use the supported ``yaml`` format,
    simply because it's easy to specify complex hierarchies using it.
    You can however, use the equivalent data structures in python and it will work just the same.


Single Element
--------------

DSL:

.. code-block:: python

    page.new('Card')

Direct API:

.. code-block:: python

    page.new_card()


Single Element With Single String Argument
------------------------------------------

DSL:

.. code-block:: python

    page.new('Card: This is the card text')

Direct API:

.. code-block:: python

    page.new_card('This is the card text')


Raw HTML
--------

DSL:

.. code-block:: python

    page.new('h1: This is the header')

Direct API:

.. code-block:: python

    page.new('h1').new_inline('This is the header')

Children
--------

DSL:

.. code-block:: python

    page.new('''
        Card:
        - Text: First Text Element
        - Text
        - Text: Second Text Element
    ''')

Direct API:

.. code-block:: python

    card = page.new_card()
    card.new_text('First Text Element')
    card.new_text()
    card.new_text('Second Text Element')

Arguments To ``new_XXX`` Methods
--------------------------------

When the first element of the children list is a list itself, it is assumed to be arguments that should be
passed to the created element.

Arguments that do not match an argument expected by the ``new_XXX`` method, are assumed to be ``props``.


DSL:

.. code-block:: python

    page.new('''
        Grid:
        - [columns: 3, className: grid-example]
        - Text: First Text Element In Grid
        - Text: Second Text Element In Grid
    ''')

Direct API:

.. code-block:: python

    grid = page.new_grid(columns=3, props={'className': 'grid-example'})
    grid.new_text('First Text Element In Grid')
    grid.new_text('Second Text Element In Grid')

List As Top Level
-----------------

An element that is specified as a list, will be converted to a ``div`` with the list as its children.

DSL:

.. code-block:: python

    page.new('''
        - Text: First Text Element
        - Text: Second Text Element
    ''')

Direct API:

.. code-block:: python

    div = page.new('div')
    div.new_text('First Text Element')
    div.new_text('Second Text Element')


Element Reference
-----------------

If the first element of an argument list is a string and not a key value pair, the resulting top level element
will contain a reference to it in its ``ref`` field.

DSL:

.. code-block:: python

    grid = page.new('''
        Grid:
        - [columns: 3]
        - Card:
          - Inline:
            - [inline1]
            - Inline Element
          - Divider: [[divider]]
    ''')
    inline1 = grid.ref.inline1
    divider = grid.ref.divider

Direct API:

.. code-block:: python

    grid = page.new_grid(columns=3)
    card = grid.new_card()
    inline1 = card.new_inline('Inline Element')
    divider = card.new_divider()


Prop Children
-------------

Certain elements accept detached root elements as their argument. ``new_panel`` is an example, where ``header`` can
be a detached element hierarchy.

You can use the intrinsic function ``{_: <ACTUAL_ELEMENT_HERE>}`` to achieve the same thing within the DSL definition.

Direct API:

.. code-block:: python

    collapse = page.new_collapse()
    _ = page.element_builder
    header = _.inline().new_icon('up-circle').n.new_inline(' Panel 1')
    collapse.new_panel(header=header)


DSL:

.. code-block:: python

    page.new('''
        Collapse:
        - Panel:
          - [header: {_: {Inline: [Icon: up-circle, Inline: ' Panel 1']}}]
    ''')


Inputs
------

Passing inputs that can be referenced in the DSL is supported by passing an additional ``inputs`` kwarg to the
``new()`` method.

In the DSL, reference the input using the intrinsic function ``{$: <INPUT_NAME>}``.

Direct API:

.. code-block:: python

    def my_function():
        print('Hello from my function')

    button = page.new_button(my_function)

DSL:

.. code-block:: python

    def my_function():
        print('Hello from my function')

    page.new('''
        Button: [[function: {$: my_function}]]
    ''', inputs={'my_function': my_function})

.. note::
    Currently, inputs can only be referenced in argument lists, but general support is planned.
