from collections import deque

import pydash
from typing import List  # noqa

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
        self._removed = False

    def new_grid(self, columns, **kwargs):
        """
        Add a grid child.

        Grid children created with ``new_XXX`` methods can provide an additional ``cols`` argument which defaults to 1.
        Element flow is left, right, top, down.

        :param columns: Number of columns for the grid.
        :return: The created grid element.
        """
        return self._new_child(Grid, columns=columns, **kwargs)

    def new_tabs(self, **kwargs):
        """
        Add a tabs child.

        The only valid ``new_XXX`` method on tabs is ``new_tab``.

        :return: The created tabs element.
        """
        return self._new_child(Tabs, **kwargs)

    def new_table(self, headers, page_size=None, **kwargs):
        """
        Add a table child.

        :param headers: list of string headers or dict, in which case, it's keys are used.
        :param page_size: Optionally, enable table pagination by specifying a page size.
        :return: The created table element.
        """
        return self._new_child(Table, headers=headers, page_size=page_size, **kwargs)

    def new_button(self, function, text='', icon=None, shape=None, type='default', block=False, **kwargs):
        """
        Add a button child.

        Most properties here are passed as is to the underlying ant-design button component, so refer
        to its documentation for more information.

        https://ant.design/components/button

        :param function: The python function that should be invoked then the button is clicked.
        :param text: Option text for the button, the function name is used by default (unless shape is supplied).
        :param icon: See ant design icon documentation.
        :param type: Any of: ``default`` (which is the default), ``primary``, ``ghost``, ``dashed``, ``danger``.
        :param shape: Optionally pass ``circle`` for a circle shaped button.
        :param block: Pass ``True`` to make the button fit the full width of its parent element.
        :return: The created button element.
        """
        return self._new_child(
            Button,
            function=function,
            text=text,
            icon=icon,
            shape=shape,
            type=type,
            block=block,
            **kwargs
        )

    def new_input(self, placeholder=None, on_enter=None, **kwargs):
        """
        Add an input child.

        :param placeholder: Optional placeholder text for the input.
        :param on_enter: Option function to be called when enter is pressed in the input.
        :return: The created input element.
        """
        return self._new_child(Input, placeholder=placeholder, on_enter=on_enter, **kwargs)

    def new_card(self, text='', **kwargs):
        """
        Add a card child.

        A card is a small padded box.

        :param text: Optional text for the card. Otherwise, use ``new_XXX`` methods as usual.
        :return: The created card element.
        """
        return self._new_child(Card, text=text, **kwargs)

    def new_text(self, text='', **kwargs):
        """
        Add a text child.

        :param text: Optional text, otherwise, interpreted as line break. ``\\n`` will be interpreted correctly.
        :return: The created text element.
        """
        return self._new_child(Text, text=text, **kwargs)

    def new_divider(self, **kwargs):
        """
        Add a divider child.

        A divider is a simple horizontal separator.

        :return: The created divider element.
        """
        return self._new_child(Divider, **kwargs)

    def new_collapse(self, **kwargs):
        """
        Add a collapse child.

        The only valid ``new_XXX`` method on collapse is ``new_panel``.

        :return: The created collapse element.
        """
        return self._new_child(Collapse, **kwargs)

    def new_chart(self, data=None, options=None, transform=None, moving_window=None, **kwargs):
        """
        Add a chart child.

        :param data: A list of data items. Each data item is expected to match the format the transformer expects.
                     A data item may also be supplied in the form of a 2-tuple (time, data),
                     in which case, the first item is the epoch time in seconds with ms precision and
                     the second item is the data item itself.
        :param options: Optional highcharts options object.
        :param transform: A transformer for the supplied data which transforms the data into suitable highcharts charts
                          and series definitions. Can be either a transformer object, a dict with transformer
                          configuration or a string specifying the transformer name.
        :param moving_window: Optional moving window size in seconds. If specified, chart will maintain this window
                              size.
        :return: The created chart element.
        """
        from .chart import Chart
        return self._new_child(
            Chart,
            data=data,
            options=options,
            transform=transform,
            moving_window=moving_window,
            **kwargs
        )

    def new_icon(self, type, theme='outlined', spin=False, two_tone_color=None, **kwargs):
        """
        Add a new icon element.

        Most properties here are passed as is to the underlying ant-design icon component, so refer
        to its documentation for more information.

        https://ant.design/components/icon

        :param type: The icon type. See ant design icon documentation.
        :param theme: Any of: ``outlined`` (the default), ``filled``, ``twoTone``
        :param spin: Pass ``True`` to make the icon spin.
        :param two_tone_color: When theme is ``twoTone``, a CSS style color for the main color of the icon.
        :return: The created icon element.
        """
        return self._new_child(Icon, type=type, theme=theme, spin=spin, two_tone_color=two_tone_color, **kwargs)

    def new_inline(self, text='', **kwargs):
        """
        Add a new inline element.

        Useful in combination with icons. As opposed to ``new_text``, ``new_inline`` doesn't take up a full line
        when added (a span is used internally).

        :param text: Optional text for the inline. Inline can also be a container element.
        :return: The created inline element.
        """
        return self._new_child(Inline, text=text, **kwargs)

    def remove(self, element=None):
        """
        Remove an element from the page.

        :param element: If supplied, remove the supplied element, otherwise, remove self.
        """
        element = element or self
        parent = element.parent
        assert parent
        return parent._remove_child(element)

    def update_data(self, data):
        """
        Update element data.

        Mostly used by element implementations but can be used for some low level updates.

        :param data: The data to update.
        """
        self.data.update(data)
        if not self._init_complete:
            return
        self.update_element(path=['data'], action='set', data=self._prepare_data(self.data))

    def update_props(self, props, override=True):
        """
        Update element props (underlying react component props).

        Mostly used by element implementations but can be used for some low level updates.

        :param props: The props to update.
        :param override: Should the supplied props override existing props. (default: ``True``)
        """
        final_props = props
        if not override:
            final_props = {k: v for k, v in props.items() if k not in self.props}
        self.props.update(final_props)
        if not self._init_complete:
            return
        self.update_element(path=['props'], action='set', data=self.props)

    def update_prop(self, path, value):
        """
        Update a prop inner value.

        Mostly used by element implementations but can be used for some low level updates.

        :param path: The nested path of the prop. If the prop is named ``A`` then reaching ``A.b.c`` would be
                    ``['A', 'b', 'c']``.
        :param value: The value to set in the nested prop path.
        """
        if isinstance(path, str):
            path = [path]
        pydash.set_(self.props, path, value)
        if not self._init_complete:
            return
        self.update_element(path=['props'] + path, action='set', data=value)

    def update_element(self, path, action, data):
        """
        Very low level method that dispatches an ``updateElement`` action to the react application running the page.
        Usually preceded by an internal element data update.
        """
        assert not self._removed
        self._dispatch({
            'type': 'updateElement',
            'id': self.id,
            'updateData': {
                'path': path,
                'action': action,
                'data': data
            }
        })

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
        assert not self._removed
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

    def _remove_child(self, element):
        if element._removed:
            return
        assert not self._removed
        ids = element._remove()
        self._increase_version()
        self.children.remove(element)
        self._dispatch({
            'type': 'removeElements',
            'ids': ids
        })
        return ids

    def _new_variable(self, value, variable_id=None):
        assert not self._removed
        self._increase_version()
        variable = variables.Variable(value, variable_id)
        self._register(variable)
        self._dispatch({
            'type': 'newVariable',
            'id': variable.id,
            'value': variable.value,
            'version': variable.version
        })
        return variable

    def _init(self, *args, **kwargs):
        pass

    def _remove(self):
        ids = [self.id]
        for child in self.children:
            ids.extend(child._remove())
        self._unregister(self)
        self._removed = True
        return ids

    def _prepare_data(self, data):
        return data

    def _register(self, obj, obj_id=None):
        self.parent._register(obj, obj_id)

    def _unregister(self, obj, obj_id=None):
        self.parent._unregister(obj, obj_id)

    def _dispatch(self, action):
        self.parent._dispatch(action)

    def _increase_version(self):
        self.parent._increase_version()


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
        self.update_props({'defaultActiveKey': []}, override=False)

    def _new_child(self, cls, **kwargs):
        assert issubclass(cls, Panel)
        return super(Collapse, self)._new_child(cls, **kwargs)

    def new_panel(self, header, active=False, **kwargs):
        """
        Add a panel child.

        :param header: The text to display as the panel header.
        :param active: Should this panel be collapsed or expanded by default. (default: False)
        :return: The created panel element.
        """

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
        """
        Get the text value.

        :return: The new text.
        """
        return self.data['text']

    @text.setter
    def text(self, value):
        """
        Set the text value.

        :param value: The new text.
        """
        self.update_data({'text': value or ''})


class Card(Text):
    allow_children = True


class Table(Element):

    allow_children = False

    def _init(self, headers, page_size):
        if isinstance(headers, dict):
            headers = list(headers.keys())
        self.update_data({'headers': headers, 'rows': deque()})
        self.update_props({
            'size': 'small',
            'pagination': {'pageSize': page_size, 'position': 'top'} if page_size else False
        }, override=False)

    def clear(self):
        """
        Clear all table rows.
        """
        if not self.data['rows']:
            return
        self.data['rows'] = deque()
        self.update_data(self.data)

    def set(self, rows):
        """
        Override existing table rows with new rows.

        :param rows: The rows to set.
        """
        self.data['rows'] = deque([self._row_data(r, i) for i, r in enumerate(rows)])
        self.update_data(self.data)

    def append(self, row):
        """
        Append a row.

        :param row: The row to append.
        """
        self._add_row(row, 'append')

    def prepend(self, row):
        """
        Prepend a row.

        :param row: The row to prepend.
        """
        self._add_row(row, 'prepend')

    def extend(self, rows):
        """
        Append several rows in one call.

        :param rows: The rows to append.
        """
        rows_data = [self._row_data(r, i) for i, r in enumerate(rows)]
        self.data['rows'].extend(rows_data)
        self.update_element(path=['data', 'rows'], action='extend', data=rows_data)

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

    def _init(self, function, text, icon, shape, type, block):
        assert (not shape) or shape == 'circle'
        self._function = function
        self._register(function, self.id)
        self.update_props({
            'icon': icon,
            'shape': shape,
            'type': type,
            'block': block
        }, override=False)
        text = text or ('' if shape else function.__name__)
        self.update_data({'text': text})

    def _remove(self):
        self._unregister(self._function, self.id)
        return super(Button, self)._remove()

    @property
    def text(self):
        """
        Get the button text.

        :return: The button text value.
        """
        return self.data['text']

    @text.setter
    def text(self, value):
        """
        Set the button text.

        :param value: The new text.
        """
        self.update_data({'text': value})


class Input(Element):

    allow_children = False

    def _init(self, placeholder, on_enter):
        self._on_enter = on_enter
        self._variable = self._new_variable('', self.id)
        if placeholder:
            self.update_props({'placeholder': placeholder}, override=False)
        if on_enter:
            self.update_data({'enter': True})
            self._register(on_enter, self.id)

    def _remove(self):
        self._unregister(self._variable, self.id)
        if self._on_enter:
            self._unregister(self._on_enter, self.id)
        return super(Input, self)._remove()


class Tabs(Element):

    def _init(self):
        self.update_props({'size': 'small', 'animated': False}, override=False)

    def _new_child(self, cls, **kwargs):
        assert issubclass(cls, Tab)
        return super(Tabs, self)._new_child(cls, **kwargs)

    def new_tab(self, name, **kwargs):
        """
        Add a tab child.

        :param name: The name of the tab.
        :return: The created tab element.
        """
        return self._new_child(Tab, name=name, **kwargs)


class Tab(Element):

    def _init(self, name):
        self.update_props({'tab': name}, override=False)


class Icon(Element):

    def _init(self, type, theme, spin, two_tone_color):
        assert theme in ['outlined', 'filled', 'twoTone']
        assert (not two_tone_color) or theme == 'twoTone'
        self.update_props({
            'type': type,
            'theme': theme,
            'spin': spin,
            'twoToneColor': two_tone_color
        }, override=False)


class Inline(Text):
    allow_children = True
