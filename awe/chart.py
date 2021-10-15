import time

import six

from .view import Element, builtin

number_types = (int, float)
timed_tuple_types = (list, tuple)
to_ms = (lambda s: int(s * 1000))
now_ms = (lambda: to_ms(time.time()))


class Transformer(object):
    key = 'base'

    def add(self, existing_data, added_data):
        transformed_added_data = self.transform(added_data)
        for config in transformed_added_data.values():
            added_series = config['series']
            existing_series = existing_data.setdefault(config['title'], {
                'title': config['title'],
                'type': config['type'],
                'series': []
            })['series']
            existing_series_set = set()
            new_series_dict = {}
            for series in existing_series:
                existing_series_set.add(series['name'])
            for series in added_series:
                if series['name'] in existing_series_set:
                    new_series_dict[series['name']] = series['data']
                else:
                    existing_series.append(series)
            for series in existing_series:
                if series['name'] in new_series_dict:
                    series['data'].extend(new_series_dict[series['name']])
        return transformed_added_data

    def transform(self, data):
        raise NotImplementedError

    @staticmethod
    def _extract_timed_tuple(now, item):
        if isinstance(item, timed_tuple_types) and len(item) == 2:
            now, item = item
            now = to_ms(now)
        return now, item


class NoOpTransformer(Transformer):
    """
    The default transformer.

    Assumes data is already in appropriate highcharts format.

    key: ``noop``
    """

    key = 'noop'

    def transform(self, data):
        return data


class NumberSequenceTransformer(Transformer):
    """
    A numbers transformer.

    Assumes each item in data is a single number or a list of numbers.

    If a list of numbers is supplied, each number in the list is assumed to belong to a different series.

    key: ``numbers``
    """

    key = 'numbers'

    def transform(self, data):
        now = now_ms()
        series_dict = {}
        for item in data:
            now, item = self._extract_timed_tuple(now, item)
            if isinstance(item, number_types):
                item = [item]
            for index, value in enumerate(item):
                series_dict.setdefault(index, {'name': index + 1, 'data': []})['data'].append((now, value))
        return {
            '': {
                'series': [series_dict[index] for index in sorted(series_dict)],
                'title': '',
                'type': 'line'
            }
        }


class FlatDictTransformer(Transformer):

    key = 'flat'

    def __init__(self, chart_mapping, series_mapping, value_key):
        """
        A transformer that expects data items to be dictionaries.

        key: ``flat``

        :param chart_mapping: A list of keys to build charts from. (combinations of them)
        :param series_mapping: A list of keys to build chart series from. (combinations of them)
        :param value_key: The key to the value of the data item.
        """
        self._chart_mapping = chart_mapping
        self._series_mapping = series_mapping
        self._value_key = value_key

    def transform(self, data):
        data = data or []
        now = now_ms()
        result = {}
        chart_dict = {}
        for item in data:
            now, item = self._extract_timed_tuple(now, item)
            chart_key = ' '.join(item[k] for k in self._chart_mapping)
            series_key = ' '.join(item[k] for k in self._series_mapping)
            value = item[self._value_key]
            current_chart = chart_dict.setdefault(chart_key, {})
            series_data = current_chart.setdefault(series_key, [])
            series_data.append((now, value))
        for chart_key, series in chart_dict.items():
            for series_key, series_data in series.items():
                (result.setdefault(chart_key, {
                    'series': [],
                    'title': chart_key,
                    'type': 'line'
                })['series'].append({
                    'name': series_key,
                    'data': series_data
                }))
        return result


class DictLevelsTransformer(Transformer):

    def __init__(self, chart_mapping, series_mapping):
        """
        A transformer that handles nested dictionaries data items.

        Usually instantiated by supplying a transform key in this format: ``[chart levels]to[series levels]``.

        For example, a key of ``23to1`` assumes a "3 level" nested dictionary where the charts will be generated
        from the different combinations of keys in the 2nd and 3rd levels and the series for each chart will be
        generated from each key in the 1st level.

        key: ``[Ns]to[Ms]``
        """

        self._chart_mapping = chart_mapping
        self._series_mapping = series_mapping

    @staticmethod
    def from_str(str_mapping):
        split = str_mapping.split('to')
        if len(split) == 2 and split[0].isdigit() and split[1].isdigit():
            chart_mapping = [int(c) for c in split[0]]
            series_mapping = [int(c) for c in split[1]]
            return DictLevelsTransformer(chart_mapping, series_mapping)
        return None

    @property
    def key(self):
        from_key = ''.join(str(k) for k in self._chart_mapping)
        to_key = ''.join(str(k) for k in self._series_mapping)
        return '{}to{}'.format(from_key, to_key)

    def transform(self, data):
        data = data or []
        now = now_ms()
        result = {}
        chart_dict = {}
        for item in data:
            now, item = self._extract_timed_tuple(now, item)
            for path, value in self._iterate_paths(item, []):
                self._process_path(chart_dict, now, path, value)
        for chart_key, series in chart_dict.items():
            for series_key, series_data in series.items():
                (result.setdefault(chart_key, {
                    'series': [],
                    'title': chart_key,
                    'type': 'line'
                })['series'].append({
                    'name': series_key,
                    'data': series_data
                }))
        return result

    def _iterate_paths(self, level, current_path):
        for level_key, level_value in level.items():
            level_path = current_path[:] + [level_key]
            if isinstance(level_value, dict):
                for (inner_level_path, inner_level_value) in self._iterate_paths(level_value, level_path):
                    yield inner_level_path, inner_level_value
            else:
                yield level_path, level_value

    def _process_path(self, chart_dict, now, path, value):
        level_to_key = {i+1: level for i, level in enumerate(path)}
        chart_key = ' '.join(level_to_key[k] for k in self._chart_mapping)
        series_key = ' '.join(level_to_key[k] for k in self._series_mapping)
        current_chart = chart_dict.setdefault(chart_key, {})
        series_data = current_chart.setdefault(series_key, [])
        series_data.append((now, value))


transformers = {t.key: t for t in [
    NoOpTransformer(),
    NumberSequenceTransformer(),
]}

transformer_classes = {t.key: t for t in [
    FlatDictTransformer
]}


@builtin
class Chart(Element):

    allow_children = False
    _transformer = None

    def _init(self, data=None, options=None, transform=None, moving_window=None):
        self.transformer = transform
        self.update_data({
            'data': self.transformer.transform(data),
            'options': options or {},
            'movingWindow': moving_window
        })

    def add(self, data):
        """
        Add new data to a chart after it has been created.

        :param data: A list of data items. Each data item is expected to match the format the transformer expects.
                     A data item may also be supplied in the form of a 2-tuple (or a list) of (time, data),
                     in which case, the first item is the epoch time in seconds with ms precision and
                     the second item is the data item itself.
        """
        transformed_data = self.transformer.add(self.data['data'], data)
        self.update_element(
            path=['data', 'data'],
            action='addChartData',
            data=transformed_data
        )

    def set(self, data):
        """
        Override existing chart data with new data.

        :param data: A list of data items. Each data item is expected to match the format the transformer expects.
                     A data item may also be supplied in the form of a 2-tuple (or a list) of (time, data),
                     in which case, the first item is the epoch time in seconds with ms precision and
                     the second item is the data item itself.
        """
        transformed_data = self.transformer.transform(data)
        self.data['data'] = transformed_data
        self.update_element(
            path=['data', 'data'],
            action='set',
            data=transformed_data
        )

    @property
    def transformer(self):
        """
        :return: The currently set transformer.
        """
        return self._transformer

    @transformer.setter
    def transformer(self, value):
        """
        Sets the transformer for the chart.
        """
        self._transformer = self._get_transformer(value)

    @staticmethod
    def _get_transformer(transform):
        transformer = transform or 'noop'
        if isinstance(transformer, Transformer):
            return transformer
        elif isinstance(transformer, dict):
            transformer_key = transformer.pop('type')
            return transformer_classes[transformer_key](**transformer)
        if isinstance(transformer, six.string_types):
            if transformer in transformers:
                return transformers[transformer]
            maybe_dict_transformer = DictLevelsTransformer.from_str(transformer)
            if maybe_dict_transformer:
                transformers[maybe_dict_transformer.key] = maybe_dict_transformer
                return maybe_dict_transformer
        raise ValueError('No matching transformer found for {}'.format(transform))
