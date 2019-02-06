from collections import deque

import pydash
import six
from typing import List  # noqa

from . import variables
from . import element_updater


builtin_element_types = {}


def builtin(cls):
    builtin_element_types[cls.__name__] = cls
    return cls


class Element(object):

    allow_children = True

    def __init__(self, root, parent, element_id, props, style, stack):
        self.root = root
        self.id = element_id or str(id(self))
        self.root_id = getattr(root, 'id', self.id)
        self.element_builder = getattr(root, 'element_builder', ElementBuilder(root))
        self.element_type = type(self).__name__
        self.parent = parent  # type: Element
        self.index = len(parent.children) + 1 if isinstance(parent, Element) else 0
        self.children = []  # type: List[Element]
        self.ref = Ref()
        self.data = {}
        self.props = props or {}
        self.props['key'] = self.id
        if style:
            self.props['style'] = style
        self._prop_children = {}
        self._init_complete = False
        self._removed = False
        self._stack = stack

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

    def new_link(self, link, **kwargs):
        """
        Add a new link element.

        :param link: The link (URL)
        :return: The created link element.
        """
        props = kwargs.setdefault('props', {})
        props.setdefault('href', link)
        return self._new_child(Raw, tag='a', **kwargs)

    def new_markdown(self, source, **kwargs):
        """
        Add a new markdown element.

        :param source: The markdown source.
        :return: The created markdown element.
        """
        return self._new_child(Markdown, source=source, **kwargs)

    def new_prop(self, prop, root=None):
        """
        Create a new element based prop.

        Mostly used by element implementations but can be used for some low level updates.

        Normally, the regular ``props`` field is used to pass basic data structures to the underlying
        react components. Sometimes however, the underlying react component prop accepts a ``ReactNode`` as
        the prop value.
        In these cases, using ``new_prop`` will create a new "root" element, similar to ``Page``.
        Use the standard ``new_XXX`` methods on it to create the element hierarchy that will be passed to the underlying
        react component prop.

        Note that a prop named ``PROP_NAME`` can only be created if it doesn't already exist in ``props`` and was not
        created with a previous ``new_prop`` call.

        :param prop: The prop name.
        :param root: Optionally, use a root element built using the element builder
        :return: The created element based prop.
        """
        assert self.parent
        assert prop not in self.props
        assert prop not in self._prop_children
        result = root or self._new_root()
        self._prop_children[prop] = result.id
        if self._init_complete:
            self._dispatch({
                'type': 'newPropChild',
                'id': result.id,
                'prop': prop,
                'elementRootId': self.root_id,
                'elementId': self.id
            })
        return result

    def new(self, obj, **kwargs):
        """
        This method can return different results depending on ``obj`` type.

        If ``obj`` is a class that inherits from Element, a new element of that type will be created.
        If ``obj`` is a dict or list, it will be parsed and the parser result will be created.
        If ``obj`` is a string, it will be yaml loaded and that result will be passed to the parser.

        When result is passed to the parser, an additional ``inputs`` argument can be supplied as a dict from keys
        to values that are referenced in the DSL using the ``$`` intrinsic function.

        :param obj: The ``Element`` subclass, a dict/list or a string to be passed to the parser.
        :param kwargs: Arguments that should be passed to the ``_init`` method of the created element or one of
                       ``props``, ``style``, ``id``, ``inputs`` if valid.
        :return: The created element.
        """
        from . import parser
        if CustomElement._is_custom(obj) and not obj._registered:
            self.register(obj)
        if parser.is_parsable(obj):
            context = parser.ParserContext(inputs=kwargs.pop('inputs', None))
            element_configuration = self._parse(obj, context)
            return self._new_children(element_configuration, **kwargs)
        else:
            return self._new_child(obj, **kwargs)

    def register(self, custom_element_cls):
        """
        Register a new custom element.

        Not that there is not need to explicitly call this method. When creating a new custom element,
        the element will be registered for you if it isn't already registered.

        :param custom_element_cls: A subclass of ``CustomElement``.
        """
        assert CustomElement._is_custom(custom_element_cls)
        if custom_element_cls._registered:
            return
        self._register(custom_element_cls, obj_id=custom_element_cls.__name__)
        custom_element_cls._registered = True
        self._dispatch({'type': 'refresh'})

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
        self.update_element(path=['data'], action='set', data=self.data)

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
        self.update_element(path=['props'], action='set', data=self.props)

    def update_prop(self, path, value):
        """
        Update a prop inner value.

        Mostly used by element implementations but can be used for some low level updates.

        :param path: The nested path of the prop. If the prop is named ``A`` then reaching ``A.b.c`` would be
                    ``['A', 'b', 'c']``.
        :param value: The value to set in the nested prop path.
        """
        if isinstance(path, six.string_types):
            path = [path]
        pydash.set_(self.props, path, value)
        self.update_element(path=['props'] + path, action='set', data=value)

    def update_element(self, path, action, data):
        """
        Very low level method that dispatches an ``updateElement`` action to the react application running the page.
        Usually preceded by an internal element data update.
        """
        if not self._init_complete:
            return
        assert not self._removed
        self._dispatch({
            'type': 'updatePath',
            'id': self.id,
            'rootId': self.root_id,
            'updateData': {
                'path': path,
                'action': action,
                'data': data
            }
        })

    @property
    def s(self):
        """
        Push current element to stack and return self.

        :return: self.
        """
        return self._stack_stash()

    @property
    def p(self):
        """
        Pop an element from the stack.

        :return: The popped element.
        """
        return self._stack_pop()

    @property
    def n(self):
        """
        Return the top most stack element.

        :return: The last stacked element or the current root element if none was stacked.
        """
        return self._stack_next()

    def _init(self, **kwargs):
        """
        Called after element was created with arguments supplied to its new_XXX method.
        """
        pass

    def _get_new_element_action(self):
        return {
            'type': 'newElement',
            'id': self.id,
            'rootId': self.root_id,
            'index': self.index,
            'elementType': self.element_type,
            'data': self.data,
            'parentId': (self.parent.id or None) if self.parent else None,
            'props': self.props,
            'propChildren': self._prop_children
        }

    def _get_view(self):
        result = self._get_new_element_action()
        result.pop('type')
        result['children'] = [t._get_view() for t in self.children]
        return result

    def _new_children(self, element_configuration, **kwargs):
        element_configuration['kwargs'].update(kwargs)
        roots = {}
        fields = {}

        def process(parent, conf):
            element_type = conf['element_type']
            kw = conf['kwargs']
            kw_children = conf['kwargs_children']
            prop_children = conf['prop_children']
            children = conf['children']
            field = conf['field']
            for kw_child in kw_children:
                kw_root = self._new_root()
                roots[kw_root.id] = kw_root
                kw[kw_child] = process(kw_root, kw[kw_child])
            element = parent._new_child(element_type, _awe_skip_dispatch=True, **kw)
            if field:
                fields[field] = element
            for prop, prop_child_conf in prop_children.items():
                prop_root = self._new_root()
                roots[prop_root.id] = prop_root
                process(prop_root, prop_child_conf)
                element._prop_children[prop] = prop_root.id
            for child_conf in children:
                process(element, child_conf)
            return element

        top_level = process(self, element_configuration)
        top_level.ref.refs.update(fields)
        dispatch_roots = {k: root._get_view() for k, root in roots.items()}
        dispatch_roots['root'] = [top_level._get_view()]
        self._dispatch({
            'type': 'processRoots',
            'roots': dispatch_roots
        })
        return top_level

    def _new_child(self, element_type, **kwargs):
        assert self.allow_children
        assert not self._removed
        self._increase_version()
        props = kwargs.pop('props', None)
        style = kwargs.pop('style', None)
        element_id = kwargs.pop('id', None)
        updater = kwargs.pop('updater', None)
        skip_dispatch = kwargs.pop('_awe_skip_dispatch', None)
        arg = kwargs.pop('_awe_arg', None)
        args = [arg] if arg else []
        # type: Element
        result = element_type(
            root=self.root,
            parent=self,
            element_id=element_id,
            props=props,
            style=style,
            stack=self._stack,
        )
        self._register(result)
        result._init(*args, **kwargs)
        if updater:
            self._register(element_updater.Updater(
                element=result,
                updater=updater
            ))
        result._init_complete = True
        self.children.append(result)
        if not skip_dispatch:
            self._dispatch(result._get_new_element_action())
        return result

    def _remove_child(self, element):
        if element._removed:
            return None
        assert not self._removed
        entries = element._remove()
        self._increase_version()
        self.children.remove(element)
        self._dispatch({
            'type': 'removeElements',
            'entries': entries
        })
        return entries

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

    def _new_root(self):
        assert not self._removed
        self._increase_version()
        result = Root(owner=self.root)
        self._register(result)
        return result

    def _remove(self):
        entries = [{'id': self.id, 'rootId': self.root_id, 'type': 'element'}]
        for prop_child_id in self._prop_children.values():
            entries.append({'id': prop_child_id, 'type': 'root'})
        for child in self.children:
            entries.extend(child._remove())
        self._unregister(self)
        self._removed = True
        return entries

    def _register(self, obj, obj_id=None):
        self.root._register(obj, obj_id)

    def _unregister(self, obj, obj_id=None):
        self.root._unregister(obj, obj_id)

    def _dispatch(self, action):
        self.root._dispatch(action)

    def _increase_version(self):
        self.root._increase_version()

    def _parse(self, obj, context):
        return self.root._parse(obj, context)

    def _stack_stash(self):
        self._stack.append(self)
        return self

    def _stack_pop(self):
        return self._stack.pop()

    def _stack_next(self):
        return self._stack[-1]


class Root(Element):

    def __init__(self, owner, element_id=None):
        super(Root, self).__init__(
            root=self,
            parent=None,
            element_id=element_id,
            props=None,
            style=None,
            stack=[self]
        )
        self._owner = owner  # type: Element

    def _get_view(self):
        return [t._get_view() for t in self.children]

    def _increase_version(self):
        self._owner._increase_version()

    def _register(self, obj, obj_id=None):
        self._owner._register(obj, obj_id)

    def _unregister(self, obj, obj_id=None):
        self._owner._unregister(obj, obj_id)

    def _dispatch(self, action, client_id=None):
        self._owner._dispatch(action)

    def _parse(self, obj, context):
        return self._owner._parse(obj, context)


class ElementBuilder(object):

    def __init__(self, owner):
        self._owner = owner  # type: Element

    def __call__(self, *args, **kwargs):
        root = self._owner._new_root()
        return root.new(*args, **kwargs)

    def __getattr__(self, item):
        root = self._owner._new_root()
        return getattr(root, 'new_{}'.format(item))


class Ref(object):

    def __init__(self):
        self.refs = {}

    def __getattr__(self, item):
        return self.refs.get(item)


class CustomElement(Element):
    """
    Base class for all custom element implementations.
    """

    _registered = False
    _scripts = []
    _styles = []

    @classmethod
    def _is_custom(cls, obj):
        return isinstance(obj, type) and issubclass(obj, cls)

    @classmethod
    def _js(cls):
        """
        Custom element javascript implementation and registration.

        :return: The javascript code (as a python string) that registers the underlying react component.
        """
        raise NotImplementedError


class Raw(Element):

    def _init(self, tag):
        self.update_data({'tag': tag})


@builtin
class Grid(Element):

    def _init(self, columns):
        self.update_data({'columns': columns, 'childColumns': []})
        self.update_props({'gutter': 5}, override=False)

    def _new_child(self, cls, **kwargs):
        columns = kwargs.pop('cols', 1)
        self.data['childColumns'].append(columns)
        if not kwargs.get('_awe_skip_dispatch'):
            self.update_element(['data', 'childColumns'], action='append', data=columns)
        return super(Grid, self)._new_child(cls, **kwargs)


@builtin
class Divider(Element):
    allow_children = False


@builtin
class Collapse(Element):

    def _init(self):
        self.update_props({'defaultActiveKey': []}, override=False)

    def _new_child(self, cls, **kwargs):
        assert issubclass(cls, Panel)
        return super(Collapse, self)._new_child(cls, **kwargs)

    def new_panel(self, header=None, active=False, **kwargs):
        """
        Add a panel child.

        :param header: If supplied, should be the text to display as the panel header.
                       Otherwise, the returned panel element will expose a ``header`` field.
                       This field should be used to create an element hierarchy (similar to ``Page``) that will be
                       passed as a ``ReactNode`` to the underlying ant design react ``Panel`` component.
        :param active: Should this panel be collapsed or expanded by default. (default: False)
        :return: The created panel element.
        """

        result = self._new_child(Panel, header=header, **kwargs)
        if active:
            self.props['defaultActiveKey'].append(result.id)
            self.update_props(self.props)
        return result


@builtin
class Panel(Element):

    def _init(self, header):
        if header:
            if isinstance(header, Element):
                assert header.root_id != self.root_id
                header = header.root
                self.new_prop('header', header)
            else:
                self.update_props({'header': header}, override=False)
            self.header = header
        else:
            self.header = self.new_prop('header')


@builtin
class Text(Element):

    allow_children = False

    def _init(self, text=''):
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


@builtin
class Card(Text):
    allow_children = True


@builtin
class Table(Element):

    allow_children = False

    def _init(self, headers, page_size=None):
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


@builtin
class Button(Element):

    allow_children = False

    def _init(self, function, text='', icon=None, shape=None, type='default', block=False):
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


@builtin
class Input(Element):

    allow_children = False

    def _init(self, placeholder=None, on_enter=None):
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
        result = super(Input, self)._remove()
        result.append({'id': self.id, 'type': 'variable'})
        return result


@builtin
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


@builtin
class Tab(Element):

    def _init(self, name):
        self.update_props({'tab': name}, override=False)


@builtin
class Icon(Element):

    def _init(self, type, theme='outlined', spin=False, two_tone_color=None):
        assert theme in ['outlined', 'filled', 'twoTone']
        assert (not two_tone_color) or theme == 'twoTone'
        self.update_props({
            'type': type,
            'theme': theme,
            'spin': spin,
            'twoToneColor': two_tone_color
        }, override=False)


@builtin
class Inline(Text):
    allow_children = True


@builtin
class Markdown(Element):
    allow_children = False

    def _init(self, source):
        self.update_props({'source': source}, override=False)
