from awe import api

from ..infra import element_tester, driver, page


def test_button(element_tester):
    button1_class = 'button1'
    button2_class = 'button2'
    button3_class = 'button3'
    button4_class = 'button4'
    button5_class = 'button5'
    button6_class = 'button6'
    button2_text = 'button2 text'
    button3_text = 'button3 text'
    button5_text = 'button5 text'
    button6_text = 'button6 text'
    button2_new_text = 'button2 new text'

    state = {}

    def button1_fn():
        state['button1_clicked'] = True

    def button2_fn():
        state['button2_clicked'] = True

    def builder(page):
        def stub():
            pass
        state['button1'] = page.new_button(button1_fn, props={'className': button1_class})
        state['button2'] = page.new_button(button2_fn, button2_text, props={'className': button2_class})
        state['button3'] = page.new_button(stub, button3_text, icon='up-circle', props={'className': button3_class})
        state['button4'] = page.new_button(stub, shape='circle', props={'className': button4_class})
        state['button5'] = page.new_button(stub, button5_text, type='primary', props={'className': button5_class})
        state['button6'] = page.new_button(stub, button6_text, block=True, props={'className': button6_class})

    def finder(driver):
        button1 = driver.find_element_by_class_name(button1_class)
        button2 = driver.find_element_by_class_name(button2_class)
        button3 = driver.find_element_by_class_name(button3_class)
        button4 = driver.find_element_by_class_name(button4_class)
        button5 = driver.find_element_by_class_name(button5_class)
        button6 = driver.find_element_by_class_name(button6_class)
        for button in [button1, button2, button3, button4, button5, button6]:
            assert button.tag_name == 'button'
        assert button1.text == button1_fn.__name__
        assert button2.text == button2_text
        assert button3.text == button3_text
        assert button4.text == ''
        assert button5.text == button5_text
        assert button6.text == button6_text
        button3.find_element_by_class_name('anticon-up-circle')
        assert 'ant-btn-circle' in button4.get_attribute('class')
        assert 'ant-btn-primary' in button5.get_attribute('class')
        assert button6.size['width'] == api.DEFAULT_WIDTH
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
