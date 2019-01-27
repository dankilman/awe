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



### [hello_world.py](examples/hello_world.py) ([static demo](https://s3.amazonaws.com/awe-static-files/examples/hello_world.html))

The most basic page with a single text element.

```python
from awe import Page


def main():
    page = Page()
    page.new_text('Hello World!')
    page.start(block=True)


if __name__ == '__main__':
    main()

 ```
![image](https://s3.amazonaws.com/awe-static-files/examples/hello_world.png)

### [chart_simple.py](examples/chart_simple.py) ([static demo](https://s3.amazonaws.com/awe-static-files/examples/chart_simple.html))

A page with a single chart.

The chart is initialized with a single data item and then updated every 1 second with a new data item.

The data added to the chart is transformed by the `numbers` transformer. It builds a single chart with series
built from each value in the data item (which is a list of numbers)

```python
import time
from random import randint

from awe import Page


def generate_random_data(size, num_series):
    result = []
    for _ in range(size):
        item = []
        for i in range(num_series):
            item.append(randint(i*100, i*100 + 100))
        result.append(item)
    return result


def main():
    args = (1, 3)
    page = Page()
    data = generate_random_data(*args)
    chart = page.new_chart(data=data, transform='numbers')
    page.start()
    while True:
        time.sleep(1)
        chart.add(generate_random_data(*args))


if __name__ == '__main__':
    main()

 ```
![image](https://s3.amazonaws.com/awe-static-files/examples/chart_simple.gif)

### [chart_complex.py](examples/chart_complex.py) ([static demo](https://s3.amazonaws.com/awe-static-files/examples/chart_complex.html))

A page with a single chart.

The chart is initialized with a single data item and then updated every 5 seconds.

The chart has a moving time window of 3 minutes.

The data added to the chart is transformed by the `2to31` transformer. It builds charts from the different keys
of the 2nd level in the nested dictionary data items. It builds the chart series from the different combinations
of the 3rd and 1st levels in the nested dictionary data items.

In general, every `[Ns...]to[Ms...]` transformer is supported.

```python
import time
from random import randint

from awe import Page


def generate_random_data(size):
    level3 = lambda: {'l3_key1': randint(0, 1000), 'l3_key2': randint(0, 1000)}
    level2 = lambda: {'l2_key1': level3(), 'l2_key2': level3(), 'l2_key3': level3()}
    level1 = lambda: {'l1_key1': level2(), 'l1_key2': level2()}
    return [level1() for _ in range(size)]


def main():
    page = Page()
    data = generate_random_data(1)
    chart = page.new_chart(data=data, transform='2to31', moving_window=3 * 60)
    page.start()
    while True:
        time.sleep(5)
        chart.add(generate_random_data(1))


if __name__ == '__main__':
    main()

 ```
![image](https://s3.amazonaws.com/awe-static-files/examples/chart_complex.gif)

### [chart_flat.py](examples/chart_flat.py) ([static demo](https://s3.amazonaws.com/awe-static-files/examples/chart_flat.html))

A page with a single chart.

The chart is initialized with a single data item and then updated every 0.7 seconds with a new data item.

The chart has a moving time window of 3 minutes.

The data added to the chart is transformed by the `flat` transformer. It builds charts from the different combinations
of the `chart_mapping` list. It builds the chart series from the different combinations
of the `series_mapping` list. The values are extracted from the `value_key` key.

```python
import time
import random

from awe import Page


def generate_random_data():
    return [{
        'color': random.choice(['blue', 'yellow']),
        'fruit': random.choice(['apple', 'orange']),
        'temp': random.choice(['cold', 'hot']),
        'city': random.choice(['Tel Aviv', 'New York']),
        'value': random.randint(1, 100)
    }]


def main():
    page = Page()
    data = generate_random_data()
    chart = page.new_chart(data=data, transform={
        'type': 'flat',
        'chart_mapping': ['color', 'fruit'],
        'series_mapping': ['temp', 'city'],
        'value_key': 'value'
    }, moving_window=3 * 60)
    page.start()
    while True:
        time.sleep(0.7)
        chart.add(generate_random_data())


if __name__ == '__main__':
    main()

 ```
![image](https://s3.amazonaws.com/awe-static-files/examples/chart_flat.gif)

### [page_properties.py](examples/page_properties.py) ([static demo](https://s3.amazonaws.com/awe-static-files/examples/page_properties.html))

A page that demonstrates how to set the page title, width and override its style.

```python
from awe import Page


def main():
    page = Page('Page Properties', width=600, style={
        'backgroundColor': 'red'
    })
    page.new_card('hello')
    page.start(block=True)


if __name__ == '__main__':
    main()

 ```
![image](https://s3.amazonaws.com/awe-static-files/examples/page_properties.png)

### [button_and_input.py](examples/button_and_input.py) ([static demo](https://s3.amazonaws.com/awe-static-files/examples/button_and_input.html))

A page with a button and two inputs.

Clicking the button or hitting enter when the second input is focused, runs `do_stuff`
which gets a reference to the input values and the button element using the `@inject` decorator.

`do_stuff` in turn, updates the button text.

```python
from awe import Page, inject


@inject(variables=['input1', 'input2'], elements=['button1'])
def do_stuff(input1, input2, button1):
    text = '{} {} {}'.format(button1.count, input1, input2)
    button1.text = text
    button1.count += 1


def main():
    page = Page()
    b = page.new_button(do_stuff, id='button1')
    b.count = 0
    page.new_input(id='input1')
    page.new_input(
        placeholder='Input 2, write anything!',
        on_enter=do_stuff,
        id='input2'
    )
    page.start(block=True)


if __name__ == '__main__':
    main()

 ```
![image](https://s3.amazonaws.com/awe-static-files/examples/button_and_input.gif)

### [standard_output.py](examples/standard_output.py) ([static demo](https://s3.amazonaws.com/awe-static-files/examples/standard_output.html))

A page that demonstrates adding text dynamically to a page after it has been started.

The elements are created with a custom style.
 
```python
import time

from awe import Page


def main():
    page = Page()
    page.start()
    page.new_text('Header', style={'fontSize': '1.5em', 'color': '#ff0000'})
    for i in range(20):
        page.new_text('{} hello {}'.format(i, i), style={'color': 'blue'})
        time.sleep(2)
    page.block()


if __name__ == '__main__':
    main()

 ```
![image](https://s3.amazonaws.com/awe-static-files/examples/standard_output.gif)

### [collapse.py](examples/collapse.py) ([static demo](https://s3.amazonaws.com/awe-static-files/examples/collapse.html))

A page with a single collapse element. 

The collapse has 3 panels. The first panel defaults to being expanded. The other two panels default to collapsed.

```python
from awe import Page


def main():
    page = Page()
    collapse = page.new_collapse()
    panel1 = collapse.new_panel('Panel 1', active=True)
    panel1.new_text('Hello From Panel 1')
    panel2 = collapse.new_panel(active=False)
    panel2.header.new_icon('pie-chart')
    panel2.header.new_inline(' Panel 2')
    panel2.new_text('Hello From Panel2')
    panel3 = collapse.new_panel('Panel 3')
    panel3.new_text('Hello From Panel3')
    page.start(block=True)


if __name__ == '__main__':
    main()

 ```
![image](https://s3.amazonaws.com/awe-static-files/examples/collapse.png)

### [custom_element.py](examples/custom_element.py) ([static demo](https://s3.amazonaws.com/awe-static-files/examples/custom_element.html))

A page that demonstrates the creation and usage of custom elements.


```python
from awe import Page, CustomElement


class Moment(CustomElement):
    _scripts = ['https://unpkg.com/moment@2.23.0/min/moment.min.js']

    @classmethod
    def _js(cls):
        return 'register((e) => <div {...e.props}>{moment().format()}</div>);'


class Popover(CustomElement):

    def _init(self, title):
        self.update_props({'title': title})

    @classmethod
    def _js(cls):
        return '''
            register((popover) => (
                <antd.Popover {...popover.props}>
                    {popover.children}
                </antd.Popover>
            ));
        '''


def main():
    page = Page()
    popover = page.new(Popover, title='Some Title')
    popover.new_button(lambda: None, 'Hover Me!')
    content = popover.new_prop('content')
    content.new_text('line 1')
    content.new(Moment)
    page.start(block=True)


if __name__ == '__main__':
    main()

 ```
![image](https://s3.amazonaws.com/awe-static-files/examples/custom_element.png)

### [raw_html.py](examples/raw_html.py) ([static demo](https://s3.amazonaws.com/awe-static-files/examples/raw_html.html))

A page that demonstrates the creation and usage of raw html elements.

Because sometimes, all you really need is a `div`.

```python
import awe

colors = ['#b47eb3', '#fdf5bf', '#ffd5ff', '#92d1c3', '#8bb8a8']
color = lambda i: colors[i % len(colors)]


def main():
    page = awe.Page()
    grid = page.new_grid(columns=3)
    for i in range(9):
        div = grid.new('div', style={
            'height': '240px',
            'textAlign': 'center',
            'backgroundColor': color(i)
        })
        lines = div.new_grid(columns=1)
        for _ in range(2):
            lines.new('br')
        lines.new('h1').new_text('Text')
        lines.new_text(str(i+1), style={
            'fontSize': '50px',
            'color': color(i+2)
        })
    page.start(block=True)


if __name__ == '__main__':
    main()

 ```
![image](https://s3.amazonaws.com/awe-static-files/examples/raw_html.png)

### [simple_report.py](examples/simple_report.py) ([static demo](https://s3.amazonaws.com/awe-static-files/examples/simple_report.html))

A page that shows how a report generation code may look like.

It demonstrates usage of `awe`'s somewhat "fluent" API
(`.s` (stash),
`.n`, (next),
`.p` (pop)).

It also shows how to pass complex data to table cells using `page.element_builder`.

It also tells the tale of Foxy Fox.

```python
import random

from awe import Page


def main():
    page = Page()
    b = page.element_builder
    page.new('h1').new_text('Simple Report')
    page.new_text('''Things weren't always so good for Foxy Fox.
                     There were days when Fox had to do {thing}, which was hard and not very satisfying.
    '''.format(thing='documentation'))
    page.new('div').s.new_inline('But things are ').n.new('em').new_inline('better').n.new_inline(' now.')
    page.new_text()
    table = page.new_table(['Day', 'Number Of Emotions'])
    for i in range(5):
        number = random.randint(0, 1000)
        url = 'https://www.google.com/search?q={}'.format(number)
        table.append([
            'Day {}'.format(i),
            b.link(url).s.new('em').new_inline(str(number)).n.new_inline(' Emotions')
        ])
    page.start(block=True)


if __name__ == '__main__':
    main()

 ```
![image](https://s3.amazonaws.com/awe-static-files/examples/simple_report.png)

### [markdown.py](examples/markdown.py) ([static demo](https://s3.amazonaws.com/awe-static-files/examples/markdown.html))

A page that demonstrates using the markdown element.


```python
from awe import Page


def main():
    page = Page()
    page.new_markdown('''
# Hello There

This is a markdown document. Thanks react-markdown!

## Let's try a list

1. Item 1
1. Item 2
1. Item 3
    ''')
    page.start(block=True)


if __name__ == '__main__':
    main()

 ```
![image](https://s3.amazonaws.com/awe-static-files/examples/markdown.png)

### [showcase.py](examples/showcase.py) ([static demo](https://s3.amazonaws.com/awe-static-files/examples/showcase.html))

A page that showcases many (currently) available elements in `awe`.

```python
import time

from awe import Page


def main():
    now = time.time()
    page = Page('Showcase')
    grid = page.new_grid(columns=3, props={'gutter': 12})
    grid.new_card('Card 1')
    card = grid.new_card()
    tabs = grid.new_tabs()
    collapse = grid.new_collapse()
    grid.new_chart([(now+i, -i) for i in range(100)], transform='numbers')
    grid.new_table(['Header 1', 'Header 2', 'Header 3'], page_size=4).extend([
        ['Value {}'.format(i), 'Value {}'.format(i+1), 'Value {}'.format(i+2)]
        for i in range(1, 20, 3)
    ])
    grid.new_divider()
    grid.new_button(lambda: None, 'Button 1', block=True)
    grid.new_input()
    grid.new_icon('heart', theme='twoTone', two_tone_color='red')
    inline = grid.new_inline()
    card.new_text('Card Text 1')
    card.new_text('Card Text 2')
    tabs.new_tab('Tab 1').new_link('https://github.com/dankilman/awe').new_text('Tab 1 Link')
    tabs.new_tab('Tab 2').new_text('Tab 2 Text')
    tabs.new_tab('Tab 3').new_text('Tab 3 Text')
    tabs.new_tab('Tab 4').new_text('Tab 4 Text')
    collapse.new_panel('Panel 1', active=True).new_text('Panel 1 Text')
    collapse.new_panel('Panel 2').new_text('Panel 2 Text')
    collapse.new_panel('Panel 3').new_text('Panel 3 Text')
    collapse.new_panel('Panel 4').new_text('Panel 4 Text')
    collapse.new_panel('Panel 5').new_text('Panel 5 Text')
    inline.new_inline('inline 1')
    inline.new_inline('inline 2')
    inline.new_inline('inline 3')
    page.start(block=True)


if __name__ == '__main__':
    main()

 ```
![image](https://s3.amazonaws.com/awe-static-files/examples/showcase.png)

### [updater.py](examples/updater.py) ([static demo](https://s3.amazonaws.com/awe-static-files/examples/updater.html))

A page that demonstrates how to use the asynchronous updater to update created elements in the background.

```python
import random
import time


from awe import Page


def updater(card):
    while True:
        card.text = 'Got {}'.format(random.randint(1, 100))
        time.sleep(0.1 + random.random())


def main():
    page = Page()
    grid = page.new_grid(columns=3)
    for _ in range(3):
        grid.new_card(updater=updater)
    page.start(block=True)


if __name__ == '__main__':
    main()

 ```
![image](https://s3.amazonaws.com/awe-static-files/examples/updater.gif)

### [dsl.py](examples/dsl.py) ([static demo](https://s3.amazonaws.com/awe-static-files/examples/dsl.html))

A page that demonstrates how to use the element DSL by calling the `new()` method with a DSL definition.
This example calls `new()` on the `page` instance, but in general, each element exposes the same functionally,
so complex element hierarchies can be added below it using different DSL definitions.

It also showcases many different element types supported by `awe`.

The following element types are used:

- tabs
- grids
- dividers
- cards
- texts
- tables

Element data is updated using API exposed by each element type.

In addition, the `divider` element is updated using the lower level `element.update_prop()` method which updates
the underlying props of the react component.

For more information on `awe`'s DSL, please refer to [DSL](https://awe-pages.readthedocs.io/en/latest/dsl.html).

```python
import time

from awe import Page


page_layout = '''
Tabs:
- Tab:
  - [name: Tab 1]
  - Grid:
    - [columns: 3]
    - Table: [[table1, headers: [c 1, c 2, c 3], cols: 2, page_size: 5]]
    - Card:
      - Card: inner
    - Card:
      - Text: [[text1, text: 4 Text]]
      - Text: [[text2, text: 4 Text 2]]
    - Card: [[card1], 0 Time]
    - Card: '6'
    - Card: [[cols: 3], '7']
  - Divider: [[divider1]]
  - Divider
  - Table: [[table2, headers: [c 4, c 5], page_size: 5]]
- Tab:
  - [name: Tab 2]
  - Table: [[table3, headers: [c 6, c 7, c 8], page_size: 5]]
  - Table: [[table4, headers: [c 2, c 5], page_size: 5]]
'''


def run():
    page = Page()
    content = page.new(page_layout)
    ref = content.ref
    page.start()
    for i in range(1000):
        ref.table1.append([i, i ** 2, i ** 3])
        ref.table2.prepend([-i, -i * 12])
        ref.table3.append([-i, -i ** 2, -i ** 3])
        ref.table4.append([i, i * 12])
        ref.text1.text = '4 Text: {}'.format(i * 3)
        ref.text2.text = '4 Text {}'.format(i * 4)
        ref.card1.children[0].text = '{} Time: {}'.format(i, time.time())
        ref.divider1.update_prop('dashed', not ref.divider1.props.get('dashed'))
        time.sleep(5)


def main():
    try:
        run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()

 ```
![image](https://s3.amazonaws.com/awe-static-files/examples/dsl.gif)


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