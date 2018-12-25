# awe

[![CircleCI](https://circleci.com/gh/dankilman/awe.svg?style=svg)](https://circleci.com/gh/dankilman/awe)
[![PyPI version](https://badge.fury.io/py/awe.svg)](https://badge.fury.io/py/awe)

Dynamic web based reports/dashboards in python.

## Motivation:

awe use cases:
- Create a report for some data you collected in your scripts.
- Poll some data/state in your script and update a chart displaying that data.
- A replacement for print statements in your scripts that can include 
  interactive tables, charts, headers, colors, etc... with minimum fuss.

awe isn't for you if you need to:
- Do web development.
- Handle a massive amount of data. awe is quite wasteful in terms of resources. This works
  well for small-ish amounts of data. On the other hand, charts with many points will
  probably make your browser completely unresponsive (not benchmarked yet, just a hunch).

Under the hood, awe generates the page using react.

## Installation
```bash
pip install awe
```

## Examples

{% macro example(name, extension='gif') -%}
### [`{{name}}.py`](examples/{{name}}.py)
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
