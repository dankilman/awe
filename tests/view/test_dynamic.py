from ..infra import element_tester, driver, page


def test_dynamic(element_tester):
    input_class = 'input1'

    def find(class_name, text):
        def finder(driver):
            assert driver.find_element_by_class_name(class_name).text == text
        return finder

    element_tester(
        lambda p: p.new_text('hello1', props={'className': 'text1'}),
        find('text1', 'hello1'),
        lambda p: p.new_text('hello2', props={'className': 'text2'}),
        find('text2', 'hello2'),
        lambda p: p.new_text('hello3', props={'className': 'text3'}),
        find('text3', 'hello3'),
        lambda p: p.new_input(props={'className': input_class}, id=input_class),
        lambda d: d.find_element_by_class_name(input_class)
    )
