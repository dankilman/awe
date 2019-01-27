Basic
=====

The following methods apply to all elements including the root ``awe.Page`` element.

In addition to the arguments documented below, every ``new_XXX`` method accepts these optional arguments:

* ``id`` Override the generated element id. Useful with the ``@inject`` decorator.
* ``props`` Pass additional ``props`` to the underlying ``react`` component.
* ``style`` Override default element style with a javascript style object.
* ``updater`` Accepts a ``callable``, ``generator``, ``async def`` and ``async generator``.
  If passed,  will be invoked asynchronously with the created element as its single argument.
  It may be long running. A convenient way of updating elements in the background.

.. autoclass:: awe.view.Element()
    :members:
