from collections import deque

import pydash

from . import variables


class Element(object):

    def __init__(self, parent, element_id, props, style):
        self.id = element_id or str(id(self))
        self.element_type = type(self).__name__
        self.parent = parent
        self.index = len(parent.children) + 1 if isinstance(parent, Element) else 0
        self.children = []
        self.data = {}
        self.props = props or {}
        self.props['key'] = self.id
        if style:
            self.props['style'] = style
        self._init_complete = False

    def get_view(self):
        return {
            'id': self.id,
            'index': self.index,
            'elementType': self.element_type,
            'data': self.prepare_data(self.data),
            'children': [t.get_view() for t in self.children],
            'props': self.props
        }

    def get_new_element_action(self):
        return {
            'type': 'newElement',
            'id': self.id,
            'index': self.index,
            'elementType': self.element_type,
            'data': self.prepare_data(self.data),
            'parentId': (self.parent.id or None) if self.parent else None,
            'props': self.props
        }

    def _new_child(self, cls, **kwargs):
        self.increase_version()
        props = kwargs.pop('props', None)
        style = kwargs.pop('style', None)
        element_id = kwargs.pop('id', None)
        result = cls(parent=self, element_id=element_id, props=props, style=style)
        self.register(result)
        result.init(**kwargs)
        result._init_complete = True
        self.children.append(result)
        self.dispatch(result.get_new_element_action())
        return result

    def new_variable(self, value, variable_id=None):
        self.increase_version()
        variable = variables.Variable(value, variable_id)
        self.register(variable)
        return variable

    def update_data(self, data):
        self.data.update(data)
        if not self._init_complete:
            return
        self.update_element(path=['data'], action='set', data=self.prepare_data(data))

    def update_props(self, props, override=True):
        final_props = props
        if not override:
            final_props = {k: v for k, v in props.items() if k not in self.props}
        self.props.update(final_props)
        if not self._init_complete:
            return
        self.update_element(path=['props'], action='set', data=final_props)

    def update_prop(self, path, value):
        if isinstance(path, str):
            path = [path]
        pydash.set_(self.props, path, value)
        if not self._init_complete:
            return
        self.update_element(path=['props'] + path, action='set', data=value)

    def update_element(self, path, action, data):
        self.dispatch({
            'type': 'updateElement',
            'id': self.id,
            'updateData': {
                'path': path,
                'action': action,
                'data': data
            }
        })

    def init(self, *args, **kwargs):
        pass

    def prepare_data(self, data):
        return data

    def register(self, obj, obj_id=None):
        self.parent.register(obj, obj_id)

    def dispatch(self, action):
        self.parent.dispatch(action)

    def increase_version(self):
        self.parent.increase_version()

    def new_grid(self, columns, **kwargs):
        return self._new_child(Grid, columns=columns, **kwargs)

    def new_tabs(self, **kwargs):
        return self._new_child(Tabs, **kwargs)

    def new_tab(self, name, **kwargs):
        return self._new_child(Tab, name=name, **kwargs)

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

    def init(self, columns):
        self.update_data({'columns': columns, 'childColumns': []})
        self.update_props({'gutter': 5}, override=False)

    def _new_child(self, cls, **kwargs):
        columns = kwargs.pop('cols', 1)
        self.data['childColumns'].append(columns)
        self.update_element(['data', 'childColumns'], action='append', data=columns)
        return super(Grid, self)._new_child(cls, **kwargs)


class Divider(Element):
    pass


class Text(Element):

    def init(self, text):
        self.set(text)

    def set(self, text):
        self.update_data({'text': text or ''})


class Card(Text):
    pass


class Table(Element):

    def init(self, headers, page_size):
        if isinstance(headers, dict):
            headers = headers.keys()
        self.update_data({'headers': headers, 'rows': deque()})
        self.update_props({
            'size': 'small',
            'pagination': {'pageSize': page_size, 'position': 'top'} if page_size else False
        }, override=False)

    def append(self, row):
        self._add_row(row, 'append')

    def prepend(self, row):
        self._add_row(row, 'prepend')

    def extend(self, rows):
        for row in rows:
            self.append(row)

    def _add_row(self, row, action):
        if isinstance(row, dict):
            row = [row[h] for h in self.data['headers']]
        row_data = {'data': row, 'id': len(self.data['rows']) + 1}
        if action == 'append':
            self.data['rows'].append(row_data)
        else:
            self.data['rows'].appendleft(row_data)
        self.update_element(path=['data', 'rows'], action=action, data=row_data)

    def prepare_data(self, data):
        result = data.copy()
        result['rows'] = list(result['rows'])
        return result


class Button(Element):

    def init(self, function, text):
        self.register(function, self.id)
        self.update_data({'text': text or function.__name__})


class Input(Element):

    def init(self, placeholder, on_enter):
        self.new_variable('', self.id)
        if placeholder:
            self.update_props({'placeholder': placeholder}, override=False)
        if on_enter:
            self.update_data({'enter': True})
            self.register(on_enter, self.id)


class Tabs(Element):

    def init(self):
        self.update_props({'size': 'small', 'animated': False}, override=False)


class Tab(Element):

    def init(self, name):
        self.update_props({'tab': name}, override=False)
