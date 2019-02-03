import copy
import time

import pytest
import requests

from awe import Page, APIClient


def test_get_elements(page, client):
    card1 = page.new_card()
    prop1 = card1.new_prop('prop1')
    text1 = card1.new_text('Text1')
    base_expected = {
        card1.id: {
            'children_ids': [text1.id],
            'element_type': 'Card',
            'id': card1.id,
            'index': 1,
            'parent_id': 'root',
            'prop_children': {'prop1': prop1.id},
            'root_id': 'root'
        },
        text1.id: {
            'children_ids': [],
            'element_type': 'Text',
            'id': text1.id,
            'index': 1,
            'parent_id': card1.id,
            'prop_children': {},
            'root_id': 'root'
        }
    }
    assert client.get_elements() == base_expected
    data_expected = copy.deepcopy(base_expected)
    data_expected[card1.id]['data'] = {'text': ''}
    data_expected[text1.id]['data'] = {'text': 'Text1'}
    assert client.get_elements(include_data=True) == data_expected
    props_expected = copy.deepcopy(base_expected)
    props_expected[card1.id]['props'] = {'key': card1.id}
    props_expected[text1.id]['props'] = {'key': text1.id}
    assert client.get_elements(include_props=True) == props_expected
    element_expected = copy.deepcopy(base_expected[card1.id])
    element_expected.update({
        'data': {'text': ''},
        'props': {'key': card1.id}
    })
    assert client.get_element(card1.id) == element_expected


def test_new_element(page, client):
    base_expected = {
        'children_ids': [],
        'data': {'text': ''},
        'element_type': 'Card',
        'id': None,
        'parent_id': 'root',
        'prop_children': {},
        'props': {'key': None},
        'root_id': 'root'
    }

    card1 = page.new_card()
    prop1 = card1.new_prop('prop1')

    r = client.new_element('Card')
    card2 = page.children[-1]
    card2_expected = copy.deepcopy(base_expected)
    card2_expected.update({
        'index': 2,
        'id': card2.id,
        'props': {'key': card2.id}
    })
    assert r == card2_expected

    r = client.new_element('Card', params={'text': 'Card3', 'props': {'hello': 'world'}})
    card3 = page.children[-1]
    card3_expected = copy.deepcopy(base_expected)
    card3_expected.update({
        'index': 3,
        'id': card3.id,
        'props': {'key': card3.id, 'hello': 'world'},
        'data': {'text': 'Card3'}
    })
    assert r == card3_expected

    r = client.new_element('Card', element_id='card4')
    card4 = page.children[-1]
    card4_expected = copy.deepcopy(base_expected)
    card4_expected.update({
        'index': 4,
        'id': 'card4',
        'props': {'key': card4.id},
    })
    assert r == card4_expected

    r = client.new_element('Card', root_id=prop1.id)
    card5 = prop1.children[-1]
    card5_expected = copy.deepcopy(base_expected)
    card5_expected.update({
        'index': 1,
        'id': card5.id,
        'props': {'key': card5.id},
        'parent_id': prop1.id,
        'root_id': prop1.id
    })
    assert r == card5_expected

    r = client.new_element('Card', parent_id=card1.id)
    card6 = card1.children[-1]
    card6_expected = copy.deepcopy(base_expected)
    card6_expected.update({
        'index': 1,
        'id': card6.id,
        'props': {'key': card6.id},
        'parent_id': card1.id,
        'root_id': 'root'
    })
    assert r == card6_expected

    r = client.new_element('Card', new_root=True)
    card7 = page._registry.elements[r['id']]
    card7_expected = copy.deepcopy(base_expected)
    card7_expected.update({
        'index': 1,
        'id': card7.id,
        'props': {'key': card7.id},
        'parent_id': r['root_id'],
        'root_id': r['root_id']
    })
    assert r['root_id'] != 'root'
    assert r == card7_expected


def test_remove_element(page, client):
    text1 = page.new_text('Text')
    assert page.children == [text1]
    client.remove_element(text1.id)
    assert page.children == []


def test_new_prop(page, client):
    text1 = page.new_text('Text')
    r = client.new_prop(text1.id, 'prop1')
    assert text1._prop_children == {'prop1': r['id']}


def test_update_data(page, client):
    text1 = page.new_text('Text')
    client.update_data(text1.id, {'text': 'New Text'})
    assert text1.text == 'New Text'


def test_update_props(page, client):
    text1 = page.new_text('Text')
    new_props = text1.props.copy()
    new_props['prop1'] = 'value1'
    client.update_props(text1.id, new_props)
    assert text1.props['prop1'] == 'value1'
    client.update_prop(text1.id, ['prop1'], 'value2')
    assert text1.props['prop1'] == 'value2'


def test_call_method(page, client):
    table1 = page.new_table(['one', 'two', 'three'])
    client.call_method(table1.id, 'append', {'row': ['value1', 'value2', 'value3']})
    assert list(table1.data['rows']) == [{'data': ['value1', 'value2', 'value3'], 'id': 1}]


def test_variables(page, client):
    input1 = page.new_input()
    assert client.get_variables() == {
        input1.id: {
            'id': input1.id,
            'value': '',
            'version': 0
        }
    }
    assert client.get_variable(input1.id) == {
        'id': input1.id,
        'value': '',
        'version': 0
    }
    r = client.new_variable('value')
    var = page._registry.variables[r['id']]
    assert var.id == r['id']
    assert var.value == 'value'
    assert var.version == 0
    client.new_variable('value2', 'var2')
    var2 = page._registry.variables['var2']
    assert var2.value == 'value2'
    assert var2.version == 0
    client.update_variable('var2', 'value3')
    assert var2.value == 'value3'
    assert var2.version == 1


def test_call_function(page, client):
    state = {}

    def fn(**kwargs):
        state['called'] = state.get('called', 0) + 1
        state['kwargs'] = kwargs

    button = page.new_button(fn)
    client.call_function(button.id)
    assert state['called'] == 1
    assert state['kwargs'] == {}
    client.call_function(button.id, {'key1': 'value1'})
    assert state['called'] == 2
    assert state['kwargs'] == {'key1': 'value1'}


@pytest.fixture()
def page():
    result = Page()
    result.start(open_browser=False)
    return result


@pytest.fixture()
def client(page):
    result = APIClient()
    assert result.port == page._port
    error = None
    for i in range(5):
        try:
            result.get_status()
            return result
        except requests.RequestException as e:
            time.sleep(0.5)
            error = e
    raise error
