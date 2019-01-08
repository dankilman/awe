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

    assert page.root_id == 'root'
    assert page.index == 0
    assert page._version == 0

    test_element = page._new_child(TestElement, style=style)
    assert page._version == 2
    test_element2 = page._new_child(TestElement2)
    test_element3 = page._new_child(TestElement, id=test_id)
    test_element4 = test_element3._new_child(TestElement4, arg1='val1', arg2='val2')

    all_elements = [test_element, test_element2, test_element3, test_element4]
    for element in all_elements:
        assert element.root_id == 'root'

    assert page._registry.elements == {t.id: t for t in all_elements}

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


def test_update_prop():
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


def test_new_prop():
    page = Page()

    class TestElement(view.Element):
        pass

    element = page._new_child(TestElement)
    element.update_prop('other_prop', 'value')
    prop1 = element.new_prop('prop1')
    text1 = prop1.new_text('text1')
    card1 = prop1.new_card('card1')

    with pytest.raises(AssertionError):
        element.new_prop('prop1')
    with pytest.raises(AssertionError):
        element.new_prop('other_prop')

    assert element._prop_children == {'prop1': prop1}
    assert prop1.id == str(id(prop1))
    assert prop1.children == [text1, card1]


def test_remove():
    page = Page()
    t1 = page.new_text('t1')
    c1 = page.new_card()
    t2 = c1.new_text('t2')
    t3 = c1.new_text('t3')
    i1 = page.new_input(id='i1')
    i2_on_enter = lambda: None
    i2 = page.new_input(on_enter=i2_on_enter, id='i2')
    b1_fn = lambda: None
    b1 = page.new_button(b1_fn, id='b1')
    registry = page._registry

    assert not any(e._removed for e in [t1, c1, t2, t3, i1, i2, b1])
    assert {c.id for c in page.children} == {t1.id, c1.id, i1.id, i2.id, b1.id}
    assert registry.elements == {t.id: t for t in [t1, c1, t2, t3, i1, i2, b1]}
    assert registry.functions == {'i2': i2_on_enter, 'b1': b1_fn}
    assert registry.variables == {'i1': i1._variable, 'i2': i2._variable}

    def entries(li):
        return [{'type': 'element', 'id': i, 'rootId': 'root'} for i in li]

    assert t1 in page.children
    assert not t1._removed
    ids = t1.remove()
    assert ids == entries([t1.id])
    assert registry.elements == {t.id: t for t in [c1, t2, t3, i1, i2, b1]}
    assert t1 not in page.children
    assert t1._removed

    ids = c1.remove()
    assert set(e['id'] for e in ids) == {c1.id, t2.id, t3.id}
    assert c1 not in page.children
    assert c1._removed
    assert t2._removed
    assert t3._removed
    assert registry.elements == {t.id: t for t in [i1, i2, b1]}

    ids = page.remove(i1)
    assert ids == entries([i1.id]) + [{'type': 'variable', 'id': i1.id}]
    assert i1._removed
    assert i1 not in page.children
    assert registry.elements == {t.id: t for t in [i2, b1]}
    assert registry.variables == {'i2': i2._variable}

    ids = i2.remove()
    assert ids == entries([i2.id]) + [{'type': 'variable', 'id': i2.id}]
    assert i2._removed
    assert i2 not in page.children
    assert registry.elements == {t.id: t for t in [b1]}
    assert registry.variables == {}
    assert registry.functions == {'b1': b1_fn}

    ids = b1.remove()
    assert ids == entries([b1.id])
    assert b1._removed
    assert not page.children
    assert not registry.elements
    assert not registry.variables
    assert not registry.functions


def test_remove_with_prop_elements():
    page = Page()
    text1 = page.new_text()
    prop1 = text1.new_prop('prop1')
    prop2 = text1.new_prop('prop2')
    text11 = prop1.new_text()
    text12 = prop1.new_text()
    text21 = prop2.new_text()
    text22 = prop2.new_text()
    removed = text1.remove()

    def prop_removal(root, element1, element2):
        return [
            {'type': 'element', 'id': element1.id, 'rootId': root.id},
            {'type': 'element', 'id': element2.id, 'rootId': root.id},
            {'type': 'root', 'id': root.id},
        ]
    text_removal = [{'type': 'element', 'id': text1.id, 'rootId': 'root'}]
    assert ((removed == text_removal + prop_removal(prop1, text11, text12) + prop_removal(prop2, text21, text22)) or
            (removed == text_removal + prop_removal(prop2, text21, text22) + prop_removal(prop1, text11, text12)))


def test_register_validation():
    page = Page()
    with pytest.raises(AssertionError):
        page.register(view.Panel)
    with pytest.raises(AssertionError):
        page.register({})
