# awe

[![CircleCI](https://circleci.com/gh/dankilman/awe.svg?style=svg)](https://circleci.com/gh/dankilman/awe)
[![PyPI version](https://badge.fury.io/py/awe.svg)](https://badge.fury.io/py/awe)

Dynamic web based reports/dashboards in python.

## Motivation:

`awe` use cases:
- Create a report for some data you collected in your scripts.
- Poll some data/state in your script and update a chart displaying that data.
- A replacement for print statements in your scripts that can include 
  interactive tables, charts, headers, colors, etc... with minimum fuss.

`awe` isn't for you if you need to:
- Do web development.
- Handle a massive amount of data. `awe` is quite wasteful in terms of resources. This works
  well for small-ish amounts of data. On the other hand, charts with many points will
  probably make your browser completely unresponsive (not benchmarked yet, just a hunch).

Under the hood, `awe` generates the page using react.

## Why is it named `awe`?

I like short names. I initially called this package `pages` but then discovered it is already taken in `pypi`.
Finding a decent unused name is not an easy task!


## Installation
```bash
pip install awe
```

## Getting Started

The basic idea in `awe` is that you create an `awe.Page()` instance in the beginning of your script. e.g:

```python
from awe import Page
page = Page()
```

The page is built by creating a hierarchy of elements. Every element, including the root `Page` element, exposes
`new_XXX()` methods that create element children.

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

The following examples can be used as reference for the different elements that can be created with `awe`.

## Examples

{% macro example(name, extension='gif') -%}
### [`{{name}}.py`](examples/{{name}}.py)
{{ docstring(name) }}
```python
{{ load(name) }}
 ```
![image](docs/images/{{name}}.{{extension}})
{% endmacro %}

{{ example('hello_world', 'png') }}
{{ example('button_and_input') }}
{{ example('chart_simple') }}
{{ example('chart_complex') }}
{{ example('kitchen') }}
{{ example('page_properties', 'png') }}
{{ example('standard_output') }}
{{ example('collapse', 'png') }}
{{ example('chart_flat') }}
