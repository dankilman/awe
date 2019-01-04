Basic
=====

The following methods apply to all elements including the root ``awe.Page`` element.

In addition to the arguments document below, every ``new_XXX`` method accepts these optional arguments:

* ``id`` Optionally override the generated element id. Useful with the ``@inject`` decorator.
* ``props`` Pass additional ``props`` to the underlying ``react`` component.
* ``style`` Override default element style with a javascript style object.

.. autoclass:: awe.view.Element()
    :members:
