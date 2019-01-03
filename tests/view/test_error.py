from ..infra import element_tester, driver, page


error_text = 'Test Error'


def test_error_on_fn(element_tester):
    button_class = 'button1'
    state = {}

    def builder(page):
        page.new_button(raise_error, props={'className': button_class})

    def finder(driver):
        state['button'] = driver.find_element_by_class_name(button_class)

    element_tester(
        builder,
        finder,
        lambda _: state['button'].click(),
        verify_error_modal,
    )


def test_error_on_export(element_tester):
    element_class = 'element1'
    state = {}

    def builder(page):
        page._exporter.export_fn = raise_error
        page.new_input(props={'className': element_class})

    builder.validate_logs_exist = True

    def finder(driver):
        state['element'] = driver.find_element_by_class_name(element_class)

    def do_export(page):
        state['element'].click()
        state['element'].send_keys('AAE'),

    element_tester(
        builder,
        finder,
        do_export,
        verify_error_modal,
    )


def verify_error_modal(driver):
    titles = driver.find_elements_by_class_name('ant-modal-title')
    assert any(t.text == 'Error' for t in titles)
    body = driver.find_element_by_tag_name('code')
    assert 'RuntimeError: {}'.format(error_text) in body.text


def raise_error(*_):
    raise RuntimeError(error_text)
