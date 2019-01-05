import copy

import mock
import pytest

from awe import chart


def test_transformer_add():
    transformer = chart.NoOpTransformer()
    existing = {
        'c1': {
            'series': [
                {'data': [1, 2], 'name': 'c1s1'},
                {'data': [3, 4], 'name': 'c1s2'},
            ],
            'title': 'c1',
            'type': 'line'
        },
        'c2': {
            'series': [
                {'data': [5, 6], 'name': 'c2s1'},
                {'data': [7, 8], 'name': 'c2s2'},
            ],
            'title': 'c2',
            'type': 'line'
        }
    }
    new = {
        'c2': {
            'series': [
                {'data': [9, 10], 'name': 'c2s2'},
                {'data': [11, 12], 'name': 'c2s3'},
            ],
            'title': 'c2',
            'type': 'line'
        },
        'c3': {
            'series': [
                {'data': [13, 14], 'name': 'c3s1'},
                {'data': [15, 16], 'name': 'c4s2'},
            ],
            'title': 'c3',
            'type': 'line'
        }
    }
    new_copy = copy.deepcopy(new)
    transformed = transformer.add(existing, new)
    assert transformed is new
    assert new == new_copy

    assert existing == {
        'c1': {
            'series': [{'data': [1, 2], 'name': 'c1s1'},
                       {'data': [3, 4], 'name': 'c1s2'}],
            'title': 'c1',
            'type': 'line'
        },
        'c2': {
            'series': [{'data': [5, 6], 'name': 'c2s1'},
                       {'data': [7, 8, 9, 10], 'name': 'c2s2'},
                       {'data': [11, 12], 'name': 'c2s3'}],
            'title': 'c2',
            'type': 'line'
        },
        'c3': {
            'series': [{'data': [13, 14], 'name': 'c3s1'},
                       {'data': [15, 16], 'name': 'c4s2'}],
            'title': 'c3',
            'type': 'line'
        }
    }


def test_get_transformer():
    get = chart.Chart._get_transformer

    for t in [None, 'noop']:
        noop_transformer = get(t)
        assert noop_transformer is chart.transformers['noop']
        assert isinstance(noop_transformer, chart.NoOpTransformer)

    assert isinstance(get('numbers'), chart.NumberSequenceTransformer)

    class MockTransformer(chart.Transformer):
        def transform(self, data):
            pass

    mock_transformer = MockTransformer()
    assert get(mock_transformer) is mock_transformer

    flat_transformer = get({
        'type': 'flat',
        'chart_mapping': ['one', 'two'],
        'series_mapping': ['three', 'four'],
        'value_key': 'value'
    })
    assert isinstance(flat_transformer, chart.FlatDictTransformer)
    assert flat_transformer._chart_mapping == ['one', 'two']
    assert flat_transformer._series_mapping == ['three', 'four']
    assert flat_transformer._value_key == 'value'

    levels_transformer = get('135to246')
    assert isinstance(levels_transformer, chart.DictLevelsTransformer)
    assert levels_transformer._chart_mapping == [1, 3, 5]
    assert levels_transformer._series_mapping == [2, 4, 6]

    with pytest.raises(ValueError):
        get('unknown')


def test_noop_transformer():
    noop = chart.NoOpTransformer()
    data = object()
    assert noop.transform(data) is data


@mock.patch.object(chart, 'now_ms', lambda: 0)
def test_numbers_transformer():
    numbers = chart.NumberSequenceTransformer()
    transform = numbers.transform([1, 2.0])
    assert transform == {
        '': {
            'series': [
                {'data': [(0, 1), (0, 2)], 'name': 1}
            ],
            'title': '',
            'type': 'line'
        }
    }
    transform = numbers.transform([[1, 2, 3], [4, 5, 6]])
    assert transform == {
        '': {
            'series': [
                {'data': [(0, 1), (0, 4)], 'name': 1},
                {'data': [(0, 2), (0, 5)], 'name': 2},
                {'data': [(0, 3), (0, 6)], 'name': 3},
            ],
            'title': '',
            'type': 'line'
        }
    }


def test_numbers_transformer_timed_tuples():
    ts = 1000.12
    expected_ts = int(ts * 1000)
    numbers = chart.NumberSequenceTransformer()
    transform = numbers.transform([(ts, 1234)])
    assert transform == {'': {'series': [{'data': [(expected_ts, 1234)], 'name': 1}], 'title': '', 'type': 'line'}}


@mock.patch.object(chart, 'now_ms', lambda: 0)
def test_flat_transformer():
    flat = chart.FlatDictTransformer(
        chart_mapping=['one', 'two'],
        series_mapping=['three', 'four'],
        value_key='value_field'
    )
    assert flat.transform(None) == {}
    assert flat.transform([]) == {}

    transform = flat.transform([
        {'one': 'one1', 'two': 'two1', 'three': 'three1', 'four': 'four', 'value_field': 1, 'unused1': True},
        {'one': 'one1', 'two': 'two1', 'three': 'three2', 'four': 'four', 'value_field': 2, 'unused2': True},
        {'one': 'one2', 'two': 'two1', 'three': 'three1', 'four': 'four', 'value_field': 3, 'unused1': True},
        {'one': 'one2', 'two': 'two1', 'three': 'three2', 'four': 'four', 'value_field': 4, 'unused2': True},
        {'one': 'one1', 'two': 'two1', 'three': 'three1', 'four': 'four', 'value_field': 5, 'unused1': True},
        {'one': 'one1', 'two': 'two1', 'three': 'three2', 'four': 'four', 'value_field': 6, 'unused2': True},
        {'one': 'one2', 'two': 'two1', 'three': 'three1', 'four': 'four', 'value_field': 7, 'unused1': True},
        {'one': 'one2', 'two': 'two1', 'three': 'three2', 'four': 'four', 'value_field': 8, 'unused2': True},
    ])

    assert transform == {
        'one1 two1': {
            'series': [{'data': [(0, 1), (0, 5)], 'name': 'three1 four'},
                       {'data': [(0, 2), (0, 6)], 'name': 'three2 four'}],
            'title': 'one1 two1',
            'type': 'line'
        },
        'one2 two1': {
            'series': [{'data': [(0, 3), (0, 7)], 'name': 'three1 four'},
                       {'data': [(0, 4), (0, 8)], 'name': 'three2 four'}],
            'title': 'one2 two1',
            'type': 'line'
        }
    }


def test_flat_transformer_timed_tuples():
    ts = 1000.12
    expected_ts = int(ts * 1000)
    numbers = chart.FlatDictTransformer(['a'], ['b'], 'c')
    transform = numbers.transform([(ts, {'a': 'a', 'b': 'b', 'c': 1234})])
    assert transform == {'a': {'series': [{'data': [(expected_ts, 1234)], 'name': 'b'}], 'title': 'a', 'type': 'line'}}


@mock.patch.object(chart, 'now_ms', lambda: 0)
def test_dict_level_transformer():
    def generate_data(v1, v2):
        level3 = lambda: {'l3_key1': v1, 'l3_key2': v2}
        level2 = lambda: {'l2_key1': level3(), 'l2_key2': level3(), 'l2_key3': level3()}
        level1 = lambda: {'l1_key1': level2(), 'l1_key2': level2()}
        return level1()

    transformer = chart.DictLevelsTransformer.from_str('13to2')
    assert transformer.key == '13to2'

    assert transformer.transform(None) == {}
    assert transformer.transform([]) == {}

    transform = transformer.transform([generate_data(1, 2), generate_data(3, 4)])
    for k, v in transform.items():
        transform[k]['series'] = sorted(transform[k]['series'], key=lambda s: s['name'])

    assert transform == {
        'l1_key1 l3_key1': {
            'series': [{'data': [(0, 1), (0, 3)], 'name': 'l2_key1'},
                       {'data': [(0, 1), (0, 3)], 'name': 'l2_key2'},
                       {'data': [(0, 1), (0, 3)], 'name': 'l2_key3'}],
            'title': 'l1_key1 l3_key1',
            'type': 'line'
        },
        'l1_key1 l3_key2': {
            'series': [{'data': [(0, 2), (0, 4)], 'name': 'l2_key1'},
                       {'data': [(0, 2), (0, 4)], 'name': 'l2_key2'},
                       {'data': [(0, 2), (0, 4)], 'name': 'l2_key3'}],
            'title': 'l1_key1 l3_key2',
            'type': 'line'
        },
        'l1_key2 l3_key1': {
            'series': [{'data': [(0, 1), (0, 3)], 'name': 'l2_key1'},
                       {'data': [(0, 1), (0, 3)], 'name': 'l2_key2'},
                       {'data': [(0, 1), (0, 3)], 'name': 'l2_key3'}],
            'title': 'l1_key2 l3_key1',
            'type': 'line'
        },
        'l1_key2 l3_key2': {
            'series': [{'data': [(0, 2), (0, 4)], 'name': 'l2_key1'},
                       {'data': [(0, 2), (0, 4)], 'name': 'l2_key2'},
                       {'data': [(0, 2), (0, 4)], 'name': 'l2_key3'}],
            'title': 'l1_key2 l3_key2',
            'type': 'line'
        }
    }


def test_dict_level_transformer_timed_tuples():
    ts = 1000.12
    expected_ts = int(ts * 1000)
    transformer = chart.DictLevelsTransformer.from_str('1to2')
    transform = transformer.transform([(ts, {'c': {'d': 1234}})])
    assert transform == {'c': {'series': [{'data': [(expected_ts, 1234)], 'name': 'd'}], 'title': 'c', 'type': 'line'}}
