from awe import inject

from ..infra import element_tester, driver, page


def test_input(element_tester):
    input1_class = 'input1'
    input2_class = 'input2'
    input3_class = 'input3'
    placeholder_text = 'placeholder text'
    input3_typed_text = 'some typed text'

    state = {}

    @inject(variables=['input3'], elements=['input2'])
    def on_enter(input3, input2):
        state['input3_value'] = input3
        state['input2_injected'] = input2

    def builder(page):
        page.new_input(props={'className': input1_class})
        input2 = page.new_input(placeholder=placeholder_text, props={'className': input2_class}, id=input2_class)
        page.new_input(on_enter=on_enter, props={'className': input3_class}, id=input3_class)
        state['input2'] = input2

    def finder(driver):
        element1 = driver.find_element_by_class_name(input1_class)
        element2 = driver.find_element_by_class_name(input2_class)
        element3 = driver.find_element_by_class_name(input3_class)
        for e in [element1, element2, element3]:
            assert e.tag_name == 'input'
            assert e.get_attribute('type') == 'text'
        assert element2.get_attribute('placeholder') == placeholder_text
        element3.send_keys('{}\n'.format(input3_typed_text))
        assert state['input3_value'] == input3_typed_text
        assert state['input2'] is state['input2_injected']

    element_tester(builder, finder)
