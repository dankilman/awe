CLI
===

A CLI to start, query and manipulate ``awe`` pages.

Any option (argument prefixed with ``-``/``--``) that is generally speaking,
complex (``dict``, ``list``, etc...), will be ``yaml`` parsed. For example,
when running this:

.. code-block:: shell

    awe new --obj 'Text: Hello World'


``obj`` will be evaluated to ``{"Text": "Hello World"}``.


In addition, prefixing such arguments with ``@`` will load the file referenced by the option and the content of
that file will be ``yaml`` parsed. e.g.

.. code-block:: shell

    awe new --obj '@/home/dan/awe-templates/table.yaml'

Object definitions when calling ``awe new`` should follow the
:ref:`dsl` specification.

.. click:: awe.cli:cli
    :prog: awe
    :show-nested:
