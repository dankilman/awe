import pytest

from awe import view, Page


def test_base():
    page = Page()

    test_data = {'data_key': 'value1'}
    test_props = {'props_key': 'value2'}
    style = {'s1': 'v1'}
    test_id = 'test_id'

    class TestElement(view.Element):
        def _init(self):
            self.update_data(test_data)
            self.update_props(test_props)

    class TestElement2(view.Element):
        pass

    class TestElement4(view.Element):
        def _init(self, arg1, arg2):
            self.arg1 = arg1
            self.arg2 = arg2

    assert page.index == 0
    assert page._version == 0

    test_element = page._new_child(TestElement, style=style)
    assert page._version == 2
    test_element2 = page._new_child(TestElement2)
    test_element3 = page._new_child(TestElement, id=test_id)
    test_element4 = test_element3._new_child(TestElement4, arg1='val1', arg2='val2')

    assert page._registry.elements == {t.id: t for t in [test_element, test_element2, test_element3, test_element4]}

    assert page.children == [test_element, test_element2, test_element3]

    assert test_element.id == str(id(test_element))
    assert test_element.element_type == 'TestElement'
    assert test_element.parent is page
    assert test_element.index == 1
    assert test_element.data == test_data
    assert test_element.props == {'key': test_element.id, 'props_key': 'value2', 'style': style}
    assert test_element.children == []

    assert test_element2.index == 2
    assert test_element2.data == {}
    assert test_element2.props == {'key': test_element2.id}

    assert test_element3.id == test_id
    assert test_element3.children == [test_element4]

    assert test_element4.arg1 == 'val1'
    assert test_element4.arg2 == 'val2'


def test_no_allow_children():
    page = Page()

    class TestElement(view.Element):
        allow_children = False

    element = page._new_child(TestElement)
    with pytest.raises(AssertionError):
        element._new_child(TestElement)


def test_update_props():
    page = Page()

    class TestElement(view.Element):
        pass

    element = page._new_child(TestElement)
    element.update_props({'key1': 'value1', 'key2': 'value2'})
    assert element.props == {'key1': 'value1', 'key2': 'value2', 'key': element.id}
    element.update_props({'key1': 'new_value1'})
    assert element.props == {'key1': 'new_value1', 'key2': 'value2', 'key': element.id}
    element.update_props({'key1': 'newer_value1', 'key3': 'value3'}, override=False)
    assert element.props == {'key1': 'new_value1', 'key2': 'value2', 'key': element.id, 'key3': 'value3'}


def test_update_prod():
    page = Page()

    class TestElement(view.Element):
        pass

    element = page._new_child(TestElement)
    element.update_props({
        'one': {
            'two': {
                'three': 4
            }
        },
        'a': 'value'
    })
    element.update_prop(['one', 'two', 'three'], 5)
    assert element.props['one']['two']['three'] == 5
    element.update_prop('a', 'other value')
    assert element.props['a'] == 'other value'
