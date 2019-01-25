# awe

[![CircleCI](https://img.shields.io/circleci/project/github/dankilman/awe/master.svg)](https://circleci.com/gh/dankilman/awe)
[![PyPI version](https://img.shields.io/pypi/v/awe.svg?colorB=brightgreen)](https://pypi.org/project/awe)
[![Documentation](https://img.shields.io/readthedocs/awe-pages.svg)](https://awe-pages.readthedocs.io)
[![License](https://img.shields.io/github/license/dankilman/awe.svg?colorB=brightgreen)](https://github.com/dankilman/awe/blob/master/LICENSE)

Dynamic web based reports/dashboards in Python.

## Installation
```bash
pip install awe
```

## Documentation

[Read The Docs](https://awe-pages.readthedocs.io)

## Examples

{% macro example(name, extension='gif') -%}
### [{{name}}.py](examples/{{name}}.py) ([static demo](https://s3.amazonaws.com/awe-static-files/examples/{{name}}.html))

{{ docstring(name) }}
```python
{{ load(name) }}
 ```
![image](https://s3.amazonaws.com/awe-static-files/examples/{{name}}.{{extension}})
{% endmacro %}

{{ example('hello_world', 'png') }}
{{ example('chart_simple') }}
{{ example('chart_complex') }}
{{ example('chart_flat') }}
{{ example('page_properties', 'png') }}
{{ example('button_and_input') }}
{{ example('standard_output') }}
{{ example('collapse', 'png') }}
{{ example('custom_element', 'png') }}
{{ example('raw_html', 'png') }}
{{ example('simple_report', 'png') }}
{{ example('markdown', 'png') }}
{{ example('showcase', 'png') }}
{{ example('dsl') }}

## Credits

The following open source projects are used by `awe`. Thank you, open source projects.
Your contributions to this world are greatly appreciated.

- [bottle (MIT)](https://github.com/bottlepy/bottle)
- [autobahn (MIT)](https://github.com/crossbario/autobahn-python)
- [twisted (MIT)](https://github.com/twisted/twisted)
- [txaio (MIT)](https://github.com/crossbario/txaio)
- [pydash (MIT)](https://github.com/dgilland/pydash)
- [react (MIT)](https://github.com/facebook/react)
- [redux (MIT)](https://github.com/reduxjs/redux)
- [ant-design (MIT)](https://github.com/ant-design/ant-design)
- [immutable.js (MIT)](https://github.com/facebook/immutable-js)
- [lodash (MIT)](https://github.com/lodash/lodash)
- [babel (MIT)](https://github.com/babel/babel)
- [react-markdown (MIT)](https://github.com/rexxars/react-markdown)


### Not strictly open source but free for non commercial use
- [highcharts (CC for non commercial use)](https://github.com/highcharts/highcharts)
