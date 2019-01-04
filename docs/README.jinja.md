# awe

[![CircleCI](https://circleci.com/gh/dankilman/awe.svg?style=svg)](https://circleci.com/gh/dankilman/awe)
[![PyPI version](https://badge.fury.io/py/awe.svg)](https://badge.fury.io/py/awe)
[![Documentation](https://readthedocs.org/projects/awe-pages/badge/?version=latest)](https://awe-pages.readthedocs.io)

Dynamic web based reports/dashboards in Python.

[API documentation](https://awe-pages.readthedocs.io)

## What is `awe` for?

`awe` use cases:
- Create a report for some data you collected in your scripts.
- Poll some data in your script and update a chart with it.
- A replacement for print statements in your scripts that can include 
  interactive tables, charts, headers, colors, etc... with minimum fuss.

`awe` isn't for you if you need to:
- Handle large amounts of data. `awe` is quite wasteful in terms of resources. This works
  well for small-ish amounts of data. On the other hand, charts with many points will
  probably make your browser completely unresponsive.

Under the hood, `awe` generates the page using react.

## Installation
```bash
pip install awe
```

## Getting Started

Begin by creating an `awe.Page()` instance. e.g:

```python
from awe import Page
page = Page()
```

A page is built by creating a hierarchy of elements. 

Every element, including the root `Page` element, exposes `new_XXX()` methods that create element children.

These methods can create leaf elements such as `new_text()`, `new_table()`, etc... e.g:

```python
page.new_text('Hello there')
```

They can also create container elements such as `new_tabs()`, `new_card()` etc... e.g:

```python
card = page.new_card()
```

If you don't intend to dynamically add data to an element, you can simply call the `new_XXX()` method with appropriate
arguments and be done with it.

If you do plan on adding data dynamically or create some element hierarchy, then keep a reference to the created
element, returned by the `new_XXX()` call. e.g:

```python
card = page.new_card()
text = card.new_text('Text inside of card')
button = card.new_button(lambda: None)
```

The above creates a card as a child element of `page` and `text` and `button` elements as children of `card`.

Once you're done with the initial page setup, call `page.start()`. e.g:

```python
# The default call will open a browser page without blocking the script
page.start()

# This will block the script
page.start(block=True)

# This will prevent the default browser open behavior
page.start(open_browser=False)
```

The [examples](#examples) section can be used as reference for the different elements that can be created with `awe`.

## Examples

{% macro example(name, extension='gif') -%}
### [{{name}}.py](examples/{{name}}.py) ([static demo](https://s3.amazonaws.com/awe-static-files/examples/{{name}}.html))

{{ docstring(name) }}
```python
{{ load(name) }}
 ```
![image](docs/images/{{name}}.{{extension}})
{% endmacro %}

{{ example('hello_world', 'png') }}
{{ example('chart_simple') }}
{{ example('chart_complex') }}
{{ example('chart_flat') }}
{{ example('page_properties', 'png') }}
{{ example('button_and_input') }}
{{ example('standard_output') }}
{{ example('collapse', 'png') }}
{{ example('showcase', 'png') }}
{{ example('kitchen') }}

## Supported Python Versions
Tested on Python 2.7.15 and 3.7.1

Should work on many earlier versions I suppose, but haven't been tested so you can't be sure.

These days, I'm mostly working with Python 2.7, so things may unintentionally break on Python 3.
That being said, the test suite runs on both versions, so chances of that happening are not very high.

Support for Python 3 has been added after initial development, so please open an issue if something
seems broken under Python 3. In fact, open an issue if something seems broken under any Python version :)

## Export To Static HTML

At any point during the lifetime of a page you can export its current state to a standalone `html` file you can
freely share.

You can export in any of the following ways:
- Open the options by clicking the options button at the top right and then click **Export**.
- Open the options by holding `Shift` and typing `A A A` (three consecutive A's) and then click **Export**.
- Hold `Shift` and type `A A E` (two A's then E).

Note that for the keyboard shortcuts to work, the focus should be on some page content.

### Export function

By default, when you export a page, the result is simply downloaded as a static file.

You can override this default behavior by passing an `export_fn` argument when creating the `Page` instance. e.g:

```python
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
```

### Offline

You can also generate the page content offline, in python only and export it in code by calling `page.export()`.

The return value of `export` is the return value of `export_fn` which defaults to the static html content as string.

e.g:

```python
from awe import Page

def main():
    page = Page(offline=True)
    page.new_text('Hello')
    print page.export()
    # you can override the export_fn supplied during creation by passing
    print page.export(export_fn=lambda index_html: index_html[:100])
    

if __name__ == '__main__':
    main()
``` 

## Why is it named `awe`?

I like short names. I initially called this package `pages` but then discovered it is already taken in `pypi`.
Finding a decent unused name is not an easy task!

## Credits

See [Credits](CREDITS.md).
