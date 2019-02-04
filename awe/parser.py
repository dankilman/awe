import inspect

import six
import yaml

from . import view


SPECIAL_KWARGS_KEYS = {'id', 'cols', 'updater'}

_init_cache = {}


class ParserContext(object):

    def __init__(self, inputs):
        self.inputs = inputs or {}


class Parser(object):

    def __init__(self, registry):
        self.registry = registry

    def parse(self, obj, context):
        obj = _prepare(obj)
        obj = self._normalize_element(obj)
        obj = self._process_intrinsic_functions(obj, context)
        element_configuration = self._parse_dict(obj)
        return element_configuration

    def _parse_dict(self, obj):
        assert isinstance(obj, dict)
        assert len(obj) == 1
        element_configuration = {
            'kwargs': {
                'props': {}
            },
            'kwargs_children': set(),
            'prop_children': {},
            'children': [],
            'field': None
        }
        key, value = list(obj.items())[0]
        element_type, additional_kwargs = self._parse_str(key)
        element_configuration['element_type'] = element_type
        element_configuration['kwargs'].update(additional_kwargs)
        if isinstance(value, six.string_types):
            if issubclass(element_type, view.Raw):
                value = [{'Inline': value}]
            else:
                element_configuration['kwargs']['_awe_arg'] = value
                value = []
        value = value or []
        if not isinstance(value, list):
            raise ValueError('Value should be a string or a list, got: {}'.format(value))
        if value and isinstance(value[0], list):
            self._parse_element_configuration(element_configuration, element_type, value[0])
            value = value[1:]
        for item in value:
            if isinstance(item, six.string_types) and not self._is_element_type(item):
                item = {'Inline': item}
            else:
                item = self._normalize_element(item)
            child_element_configuration = self._parse_dict(item)
            element_configuration['children'].append(child_element_configuration)
        return element_configuration

    def _parse_element_configuration(self, result, element_type, configuration_items):
        if not configuration_items:
            return
        if not isinstance(configuration_items, list):
            raise ValueError('Element configuration should be passed as a list, got: {}'.format(configuration_items))
        if isinstance(configuration_items[0], six.string_types):
            result['field'] = configuration_items[0]
            configuration_items = configuration_items[1:]
        for item in configuration_items:
            assert isinstance(item, dict)
            assert len(item) == 1
            key, value = list(item.items())[0]
            is_element_value = self._is_intrinsic(value, '_')
            if is_element_value:
                value = value['_']
                value = self._normalize_element(value)
                value = self._parse_dict(value)
            if key in SPECIAL_KWARGS_KEYS or key in self._get_init_args(element_type):
                result['kwargs'][key] = value
                if is_element_value:
                    result['kwargs_children'].add(key)
            elif is_element_value:
                result['prop_children'][key] = value
            else:
                result['kwargs']['props'][key] = value

    def _parse_str(self, obj_str):
        assert obj_str
        if obj_str[0].islower():
            return view.Raw, {'tag': obj_str}
        elif obj_str in view.builtin_element_types:
            return view.builtin_element_types[obj_str], {}
        elif obj_str in self.registry.element_types:
            return self.registry.element_types[obj_str], {}
        raise ValueError('No such element: {}'.format(obj_str))

    def _is_element_type(self, str_obj):
        return (
            str_obj in self.registry.element_types or
            str_obj in view.builtin_element_types
        )

    @staticmethod
    def _is_intrinsic(obj, key):
        return isinstance(obj, dict) and len(obj) == 1 and bool(obj.get(key))

    def _process_input(self, node, context):
        input_node = self._process_intrinsic_functions(node['$'], context)
        if isinstance(input_node, six.string_types):
            input_node = [input_node]
        input_name = input_node[0]
        input_node = input_node[1:]
        default_value = None
        for entry in input_node:
            assert isinstance(entry, dict)
            assert len(entry) == 1
            key, value = list(entry.items())[0]
            if key == 'default':
                default_value = value
            else:
                raise ValueError('Unknown config option: {}'.format(key))
        if default_value:
            return context.inputs.get(input_name, default_value)
        else:
            return context.inputs[input_name]

    def _process_intrinsic_functions(self, obj, context):
        def process(node):
            if isinstance(node, dict):
                if self._is_intrinsic(node, '$'):
                    return self._process_input(node, context)
                return {k: process(v) for k, v in node.items()}
            elif isinstance(node, list):
                return [process(item) for item in node]
            return node
        return process(obj)

    @staticmethod
    def _normalize_element(obj):
        if isinstance(obj, six.string_types):
            obj = {obj: None}
        elif isinstance(obj, list):
            obj = {'div': obj}
        return obj

    @staticmethod
    def _get_init_args(element_type):
        if element_type in _init_cache:
            return _init_cache[element_type]
        result = set()
        getargspec_impl = inspect.getargspec if six.PY2 else inspect.getfullargspec
        spec = getargspec_impl(element_type._init)
        result |= set(spec.args)
        if six.PY3:
            result |= set(spec.kwonlyargs)
        _init_cache[element_type] = result
        return result


def is_parsable(obj):
    return isinstance(obj, six.string_types + (list, dict))


def _prepare(obj):
    if isinstance(obj, six.string_types):
        obj = yaml.load(obj)
    return obj
