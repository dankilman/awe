from awe import view
from awe import parser
from awe import Page


def test_is_parsable():
    assert parser.is_parsable('')
    assert parser.is_parsable({})
    assert parser.is_parsable([])

    assert not parser.is_parsable(None)
    assert not parser.is_parsable(view.Element)
    assert not parser.is_parsable(view.CustomElement)


def test_prepare():
    obj1 = object()
    assert parser._prepare(obj1) is obj1
    assert parser._prepare('one') == 'one'
    assert parser._prepare('"one"') == 'one'
    assert parser._prepare('[]') == []
    assert parser._prepare('{}') == {}


def test_parser_yaml_string_input():
    page = Page()
    result = page.new('''
        - Divider
        - span: hello
    ''')
    assert isinstance(result, view.Raw)
    assert result.data['tag'] == 'div'
    assert len(result.children) == 2


def test_parser_string_input():
    page = Page()
    result = page.new('Divider')
    assert isinstance(result, view.Divider)


def test_parser_object_input():
    page = Page()
    result = page.new({'Divider': None})
    assert isinstance(result, view.Divider)


def test_parser_list_input():
    page = Page()
    result = page.new(['Divider', {'span': 'hello'}])
    assert isinstance(result, view.Raw)
    assert result.data['tag'] == 'div'
    assert len(result.children) == 2


def test_parse_custom_element():
    class TestElement(view.CustomElement):
        @classmethod
        def _js(cls):
            pass

    page = Page()
    page.register(TestElement)
    result = page.new('TestElement')
    assert isinstance(result, TestElement)


def test_parse_inline_text():
    page = Page()
    result = page.new('span: Hello There')
    assert isinstance(result, view.Raw)
    assert len(result.children) == 1
    child = result.children[0]
    assert isinstance(child, view.Inline)
    assert child.text == 'Hello There'


def test_parse_element_configuration_variables():
    page = Page()
    result = page.new('''
        - Divider:
          - [divider1]
        - span:
          - [span1]
          - Inline: Hello There
    ''')
    assert isinstance(result.ref.divider1, view.Divider)
    assert isinstance(result.ref.span1, view.Raw)


def test_parse_element_configuration_element_prop():
    page = Page()
    result = page.new('''
        Divider:
        - [prop1: Prop1 Value]
    ''')
    assert result.props['prop1'] == 'Prop1 Value'


def test_parse_element_configuration_element_value():
    page = Page()
    result = page.new('''
        Divider:
        - [prop1: {_: {Divider: [[inner_divider]]}}]
    ''')
    assert isinstance(result.ref.inner_divider, view.Divider)
    assert result._prop_children['prop1'] == result.ref.inner_divider.root_id


def test_parse_element_configuration_element_value_init_arg():
    page = Page()
    result = page.new('''
        Collapse:
        - Panel: [[panel1, header: {_: {Text: Text 1}}]]
    ''')
    panel1 = result.ref.panel1
    assert panel1._prop_children
    assert panel1.header.children[0].text == 'Text 1'


def test_parse_element_configuration_id():
    page = Page()
    result = page.new('''
        Divider:
        - [id: divider1]
    ''')
    assert result.id == 'divider1'


def test_parse_element_configuration_cols():
    page = Page()
    result = page.new('''
        Grid:
        - [columns: 3]
        - Text: [[cols: 2]]
    ''')
    assert result.data['childColumns'] == [2]


def test_parse_element_configuration_init_arg():
    page = Page()
    result = page.new('''
        Text:
        - [text: Hello Text]
    ''')
    assert result.text == 'Hello Text'


def test_parse_element_configuration_variable_and_more():
    page = Page()
    result = page.new('''
        Divider:
        - [divider_var1, id: divider1]
    ''')
    assert result.ref.divider_var1 is result
    assert result.id == 'divider1'


def test_parse_children():
    page = Page()
    result = page.new(['Divider', 'Text'])
    children = result.children
    assert len(children) == 2
    divider, text = children
    assert isinstance(divider, view.Divider)
    assert isinstance(text, view.Text)


def test_parse_element_configuration_and_children():
    page = Page()
    result = page.new('''
        Card:
        - [id: card1]
        - Text
        - Inline
    ''')
    assert result.id == 'card1'
    children = result.children
    assert len(children) == 2
    text, inline = children
    assert isinstance(text, view.Text)
    assert isinstance(inline, view.Inline)


def test_parse_raw_element_dict_text_value():
    page = Page()
    result = page.new('span: Hello There')
    assert len(result.children) == 1
    assert isinstance(result.children[0], view.Inline)
    assert result.children[0].text == 'Hello There'


def test_parse_first_init_arg_as_dict_value():
    page = Page()
    result = page.new('Text: Hello There')
    assert result.text == 'Hello There'


def test_text_child():
    page = Page()
    result = page.new('''
        Card:
        - Card Text
    ''')
    assert result.children[0].text == 'Card Text'
