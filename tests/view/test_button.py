from ..infra import element_tester, driver, page


def test_button(element_tester):
    button1_class = 'button1'
    button2_class = 'button2'
    button2_text = 'button2 text'
    button2_new_text = 'button2 new text'

    state = {}

    def button1_fn():
        state['button1_clicked'] = True

    def button2_fn():
        state['button2_clicked'] = True

    def builder(page):
        page.new_button(button1_fn, props={'className': button1_class})
        state['button2'] = page.new_button(button2_fn, button2_text, props={'className': button2_class})

    def finder(driver):
        button1 = driver.find_element_by_class_name(button1_class)
        button2 = driver.find_element_by_class_name(button2_class)
        assert button1.tag_name == 'button'
        assert button2.tag_name == 'button'
        assert button1.text == button1_fn.__name__
        assert button2.text == button2_text
        button1.click()
        assert state['button1_clicked']
        button2.click()
        assert state['button2_clicked']

    def modifier(page):
        state['button2'].text = button2_new_text

    def finder2(driver):
        button2 = driver.find_element_by_class_name(button2_class)
        assert button2.text == button2_new_text

    element_tester(
        builder,
        finder,
        modifier,
        finder2
    )
