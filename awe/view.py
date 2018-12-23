from collections import deque

import pydash
from typing import List

from . import variables


class Element(object):

    allow_children = True

    def __init__(self, parent, element_id, props, style):
        self.id = element_id or str(id(self))
        self.element_type = type(self).__name__
        self.parent = parent  # type: Element
        self.index = len(parent.children) + 1 if isinstance(parent, Element) else 0
        self.children = []  # type: List[Element]
        self.data = {}
        self.props = props or {}
        self.props['key'] = self.id
        if style:
            self.props['style'] = style
        self._init_complete = False

    def _get_view(self):
        return {
            'id': self.id,
            'index': self.index,
            'elementType': self.element_type,
            'data': self._prepare_data(self.data),
            'children': [t._get_view() for t in self.children],
            'props': self.props
        }

    def _get_new_element_action(self):
        return {
            'type': 'newElement',
            'id': self.id,
            'index': self.index,
            'elementType': self.element_type,
            'data': self._prepare_data(self.data),
            'parentId': (self.parent.id or None) if self.parent else None,
            'props': self.props
        }

    def _new_child(self, cls, **kwargs):
        assert self.allow_children
        self._increase_version()
        props = kwargs.pop('props', None)
        style = kwargs.pop('style', None)
        element_id = kwargs.pop('id', None)
        result = cls(parent=self, element_id=element_id, props=props, style=style)  # type: Element
        self._register(result)
        result._init(**kwargs)
        result._init_complete = True
        self.children.append(result)
        self._dispatch(result._get_new_element_action())
        return result

    def _new_variable(self, value, variable_id=None):
        self._increase_version()
        variable = variables.Variable(value, variable_id)
        self._register(variable)
        return variable

    def update_data(self, data):
        self.data.update(data)
        if not self._init_complete:
            return
        self.update_element(path=['data'], action='set', data=self._prepare_data(self.data))

    def update_props(self, props, override=True):
        final_props = props
        if not override:
            final_props = {k: v for k, v in props.items() if k not in self.props}
        self.props.update(final_props)
        if not self._init_complete:
            return
        self.update_element(path=['props'], action='set', data=self.props)

    def update_prop(self, path, value):
        if isinstance(path, str):
            path = [path]
        pydash.set_(self.props, path, value)
        if not self._init_complete:
            return
        self.update_element(path=['props'] + path, action='set', data=value)

    def update_element(self, path, action, data):
        self._dispatch({
            'type': 'updateElement',
            'id': self.id,
            'updateData': {
                'path': path,
                'action': action,
                'data': data
            }
        })

    def _init(self, *args, **kwargs):
        pass

    def _prepare_data(self, data):
        return data

    def _register(self, obj, obj_id=None):
        self.parent._register(obj, obj_id)

    def _dispatch(self, action):
        self.parent._dispatch(action)

    def _increase_version(self):
        self.parent._increase_version()

    def new_grid(self, columns, **kwargs):
        return self._new_child(Grid, columns=columns, **kwargs)

    def new_tabs(self, **kwargs):
        return self._new_child(Tabs, **kwargs)

    def new_table(self, headers, page_size=None, **kwargs):
        return self._new_child(Table, headers=headers, page_size=page_size, **kwargs)

    def new_button(self, function, text='', **kwargs):
        return self._new_child(Button, function=function, text=text, **kwargs)

    def new_input(self, placeholder=None, on_enter=None, **kwargs):
        return self._new_child(Input, placeholder=placeholder, on_enter=on_enter, **kwargs)

    def new_card(self, text='', **kwargs):
        return self._new_child(Card, text=text, **kwargs)

    def new_text(self, text='', **kwargs):
        return self._new_child(Text, text=text, **kwargs)

    def new_divider(self, **kwargs):
        return self._new_child(Divider, **kwargs)

    def new_collapse(self, **kwargs):
        return self._new_child(Collapse, **kwargs)

    def new_chart(self, data=None, options=None, transform=None, moving_window=None, **kwargs):
        from .chart import Chart
        return self._new_child(
            Chart,
            data=data,
            options=options,
            transform=transform,
            moving_window=moving_window,
            **kwargs
        )


class Grid(Element):

    def _init(self, columns):
        self.update_data({'columns': columns, 'childColumns': []})
        self.update_props({'gutter': 5}, override=False)

    def _new_child(self, cls, **kwargs):
        columns = kwargs.pop('cols', 1)
        self.data['childColumns'].append(columns)
        self.update_element(['data', 'childColumns'], action='append', data=columns)
        return super(Grid, self)._new_child(cls, **kwargs)


class Divider(Element):
    allow_children = False


class Collapse(Element):

    def _init(self):
        self.update_props({'defaultActiveKey': []})

    def _new_child(self, cls, **kwargs):
        assert issubclass(cls, Panel)
        return super(Collapse, self)._new_child(cls, **kwargs)

    def new_panel(self, header, active=False, **kwargs):
        result = self._new_child(Panel, header=header, **kwargs)
        if active:
            self.props['defaultActiveKey'].append(result.id)
            self.update_props(self.props)
        return result


class Panel(Element):

    def _init(self, header):
        self.update_props({'header': header}, override=False)


class Text(Element):

    allow_children = False

    def _init(self, text):
        self.text = text

    @property
    def text(self):
        return self.data['text']

    @text.setter
    def text(self, value):
        self.update_data({'text': value or ''})


class Card(Text):
    allow_children = True


class Table(Element):

    allow_children = False

    def _init(self, headers, page_size):
        if isinstance(headers, dict):
            headers = headers.keys()
        self.update_data({'headers': headers, 'rows': deque()})
        self.update_props({
            'size': 'small',
            'pagination': {'pageSize': page_size, 'position': 'top'} if page_size else False
        }, override=False)

    def clear(self):
        if not self.data['rows']:
            return
        self.data['rows'] = deque()
        self.update_data(self.data)

    def set(self, rows):
        self.data['rows'] = deque([self._row_data(r, i) for i, r in enumerate(rows)])
        self.update_data(self.data)

    def append(self, row):
        self._add_row(row, 'append')

    def prepend(self, row):
        self._add_row(row, 'prepend')

    def extend(self, rows):
        for row in rows:
            self.append(row)

    def _add_row(self, row, action):
        row_data = self._row_data(row)
        if action == 'append':
            self.data['rows'].append(row_data)
        else:
            self.data['rows'].appendleft(row_data)
        self.update_element(path=['data', 'rows'], action=action, data=row_data)

    def _row_data(self, row, offset=0):
        if isinstance(row, dict):
            row = [row[h] for h in self.data['headers']]
        return {'data': row, 'id': len(self.data['rows']) + 1 + offset}

    def _prepare_data(self, data):
        result = data.copy()
        result['rows'] = list(result['rows'])
        return result


class Button(Element):

    allow_children = False

    def _init(self, function, text):
        self._register(function, self.id)
        self.update_data({'text': text or function.__name__})

    @property
    def text(self):
        return self.data['text']

    @text.setter
    def text(self, value):
        self.update_data({'text': value})


class Input(Element):

    allow_children = False

    def _init(self, placeholder, on_enter):
        self._new_variable('', self.id)
        if placeholder:
            self.update_props({'placeholder': placeholder}, override=False)
        if on_enter:
            self.update_data({'enter': True})
            self._register(on_enter, self.id)


class Tabs(Element):

    def _init(self):
        self.update_props({'size': 'small', 'animated': False}, override=False)

    def _new_child(self, cls, **kwargs):
        assert issubclass(cls, Tab)
        return super(Tabs, self)._new_child(cls, **kwargs)

    def new_tab(self, name, **kwargs):
        return self._new_child(Tab, name=name, **kwargs)


class Tab(Element):

    def _init(self, name):
        self.update_props({'tab': name}, override=False)
