import time

from .view import Element

number_types = (int, float, long)
now_ms = (lambda: int(time.time() * 1000))


class Transformer(object):
    key = 'base'

    def add(self, existing_data, added_data):
        transformed_added_data = self.transform(added_data)
        for config in transformed_added_data.values():
            added_series = config['series']
            existing_series = existing_data[config['title']]['series']
            new_series_dict = {}
            for series in added_series:
                new_series_dict[series['name']] = series['data']
            for series in existing_series:
                series['data'].extend(new_series_dict[series['name']])
        return transformed_added_data

    def transform(self, data):
        raise NotImplementedError


class NoOpTransformer(Transformer):
    key = 'noop'

    def transform(self, data):
        return data


class NumberSequenceTransformer(Transformer):
    key = 'numbers'

    def transform(self, data):
        now = now_ms()
        series_dict = {}
        for item in data:
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


class DictLevelsTransformer(Transformer):

    def __init__(self, chart_mapping, series_mapping):
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
        from_key = ''.join(str(l) for l in self._chart_mapping)
        to_key = ''.join(str(l) for l in self._series_mapping)
        return '{}to{}'.format(from_key, to_key)

    def transform(self, data):
        data = data or []
        now = now_ms()
        result = {}
        chart_dict = {}
        for item in data:
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
        chart_key = ' '.join(level_to_key[l] for l in self._chart_mapping)
        series_key = ' '.join(level_to_key[l] for l in self._series_mapping)
        current_chart = chart_dict.setdefault(chart_key, {})
        series_data = current_chart.setdefault(series_key, [])
        series_data.append((now, value))


transformers = {t.key: t for t in [
    NoOpTransformer(),
    NumberSequenceTransformer()
]}


class Chart(Element):

    allow_children = False
    transformer = None

    def _init(self, data, options, transform, moving_window):
        self.transformer = self._get_transformer(transform)
        self.update_data({
            'data': self.transformer.transform(data),
            'options': options or {},
            'movingWindow': moving_window
        })

    def add(self, data):
        transformed_data = self.transformer.add(self.data['data'], data)
        self.update_element(
            path=['data', 'data'],
            action='addChartData',
            data=transformed_data
        )

    @staticmethod
    def _get_transformer(transform):
        transformer = transform or 'noop'
        if isinstance(transformer, Transformer):
            return transformer
        if isinstance(transformer, basestring):
            if transformer in transformers:
                return transformers[transformer]
            maybe_dict_transformer = DictLevelsTransformer.from_str(transformer)
            if maybe_dict_transformer:
                transformers[maybe_dict_transformer.key] = maybe_dict_transformer
                return maybe_dict_transformer
        raise ValueError('No matching transformer found for {}'.format(transform))
