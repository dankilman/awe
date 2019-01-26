Export
======

At any point during the lifetime of a page you can export its current state to a standalone `html` file you can
freely share.

You can export in any of the following ways:

* Open the options by clicking the options button at the top right and then click **Export**.
* Open the options by holding ``Shift`` and typing ``A A A`` (three consecutive A's) and then click **Export**.
* Hold ``Shift`` and type ``A A E`` (two A's then E).

Note that for the keyboard shortcuts to work, the focus should be on some page content.

Export function
---------------

By default, when you export a page, the result is simply downloaded as a static file.

You can override this default behavior by passing an ``export_fn`` argument when creating the ``Page`` instance. e.g:

.. code-block:: python

    import time

    from awe import Page

    from utils import save_to_s3  # example import, not something awe comes bundled with


    def custom_export_fn(index_html):
        # index_html is the static html content as a string.
        # You can, for example, save the content to S3.
        key = 'page-{}.html'.format(time.time())
        save_to_s3(
            bucket='my_bucket',
            key=key,
            content=index_html
        )

        # Returning a dict from the export_fn function tells awe to skip the default download behavior.
        # awe will also display a simple key/value table modal built from the dict result.
        # Returning anything else is expected to be a string that will be downloaded in the browser.
        # This can be the unmodified index_html, a modified one, a json with statistics, etc...
        return {'status': 'success', 'key': key}


    def main():
        page = Page(export_fn=custom_export_fn)
        page.new_text('Hello')
        page.start(block=True)


    if __name__ == '__main__':
        main()

Offline
-------

You can also generate the page content offline, in python only and export it in code by calling ``page.export()``.

The return value of ``export`` is the return value of ``export_fn`` which defaults to the static html content as string.

e.g:

.. code-block:: python

    from awe import Page

    def main():
        page = Page(offline=True)
        page.new_text('Hello')
        print(page.export())
        # you can override the export_fn supplied during creation by passing
        print(page.export(export_fn=lambda index_html: index_html[:100]))


    if __name__ == '__main__':
        main()
