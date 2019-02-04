import json
import os
import subprocess

import pytest

from awe import Page, view


def test_start_sanity():
    env = os.environ.copy()
    env['AWE_OFFLINE'] = '1'
    subprocess.check_call([
        'awe', 'start',
        '-t', 'title1',
        '-w', '800',
        '-o', 'Text: Hello World',
        '-p', 'props: {key1: value1}',
        '-s', 'color: red',
    ], env=env)


def test_status():
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_call(['awe', 'status'])
    page = Page()
    page.start(open_browser=False)
    subprocess.check_call(['awe', 'status'])


def test_ls_and_get():
    page = Page()
    text1 = page.new_text()
    page.start(open_browser=False)
    output = subprocess.check_output(['awe', '-l', 'ls'])
    parsed_output = json.loads(output)
    assert parsed_output[text1.id]['id'] == text1.id
    output = subprocess.check_output(['awe', '-l', 'get', '-e', text1.id])
    parsed_output = json.loads(output)
    assert parsed_output['id'] == text1.id


def test_element_creation_modification_and_call():
    page = Page()
    page.start(open_browser=False)
    subprocess.check_call(['awe', 'new', '-o', 'Text: Hello World', '-p', 'props: {key1: value1}'])
    text1 = page.children[0]
    assert isinstance(text1, view.Text)
    assert text1.text == 'Hello World'
    assert text1.props['key1'] == 'value1'
    subprocess.check_call(['awe', 'new-prop', '-e', text1.id, '-n', 'prop1'])
    assert 'prop1' in text1._prop_children
    subprocess.check_call(['awe', 'update-data', '-e', text1.id, '-d', 'text: New Text'])
    assert text1.text == 'New Text'
    subprocess.check_call(['awe', 'update-props', '-e', text1.id, '-p', 'key1: value11'])
    assert text1.props['key1'] == 'value11'
    subprocess.check_call(['awe', 'update-prop', '-e', text1.id, '-p', 'key1', '-v', 'value12'])
    assert text1.props['key1'] == 'value12'
    subprocess.check_call(['awe', 'call', '-e', text1.id, '-m', 'update_props', '-k', 'props: {key1: value13}'])
    assert text1.props['key1'] == 'value13'
    subprocess.check_call(['awe', 'remove', '-e', text1.id])
    assert page.children == []


def test_variables():
    page = Page()
    input1 = page.new_input(id='input1')
    page.start(open_browser=False)
    output = subprocess.check_output(['awe', '-l', 'ls-variables'])
    parsed_output = json.loads(output)
    assert parsed_output[input1.id] == {'id': input1.id, 'value': '', 'version': 0}
    output = subprocess.check_output(['awe', '-l', 'get-variable', '-v', input1.id])
    parsed_output = json.loads(output)
    assert parsed_output == {'id': input1.id, 'value': '', 'version': 0}
    subprocess.check_call(['awe', 'new-variable', '-d', 'initial-value', '-v', 'variable1'])
    assert page._registry.variables['variable1'].get_variable() == {
        'id': 'variable1', 'value': 'initial-value', 'version': 0
    }
    subprocess.check_call(['awe', 'update-variable', '-d', 'new-value', '-v', 'variable1'])
    assert page._registry.variables['variable1'].get_variable() == {
        'id': 'variable1', 'value': 'new-value', 'version': 1
    }


def test_call_function():
    state = {}

    def fn(**kwargs):
        state.update(kwargs)

    page = Page()
    page.new_button(fn, 'function', id='button1')
    page.start(open_browser=False)
    subprocess.check_call(['awe', 'call-function', '-f', 'button1', '-k', 'key1: value1'])
    assert state == {'key1': 'value1'}
