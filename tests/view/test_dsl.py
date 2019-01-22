from ..infra import element_tester, driver, page


def test_dsl(element_tester):
    state = {}

    def builder(page):
        top_level = page.new('''
            - Text: [[text1, text: Text 1, className: text1]]
        ''')
        state['top_level'] = top_level

    def finder(driver):
        text_element = driver.find_element_by_class_name('text1')
        assert text_element.text == 'Text 1'

    def dynamic_change(page):
        top_level = state['top_level']
        top_level.ref.text1.text = 'Text 11'
        top_level.new('''
            - Text: [[text2, text: Text 2, className: text2]]
        ''')

    def verify_change(driver):
        text_element = driver.find_element_by_class_name('text1')
        text_element2 = driver.find_element_by_class_name('text2')
        assert text_element.text == 'Text 11'
        assert text_element2.text == 'Text 2'

    element_tester(
        builder,
        finder,
        dynamic_change,
        verify_change
    )
