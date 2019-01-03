import time

from ..infra import element_tester, driver, page


state = {}


def test_export_with_keyboard_shortcut(element_tester):
    _test_export(
        element_tester,
        download_export_fn,
        lambda _: state['element'].send_keys('AAE'),
    )


def test_export_with_options_keyboard_shortcut(element_tester):
    _test_export(
        element_tester,
        download_export_fn,
        lambda _: state['element'].send_keys('AAA'),
        wait_for_options_modal,
        lambda _: state['button'].click(),
    )


def test_export_with_mouse_only(element_tester):
    _test_export(
        element_tester,
        download_export_fn,
        lambda _: state['options_button'].click(),
        wait_for_options_modal,
        lambda _: state['button'].click(),
    )


def test_export_with_object_export_fn(element_tester):
    def verify_object_modal(driver):
        titles = driver.find_elements_by_class_name('ant-modal-title')
        assert any(e.text == 'Export Result' for e in titles)
        table = driver.find_element_by_class_name('ant-table-body').find_element_by_tag_name('table')
        rows = [r.text for r in table.find_elements_by_tag_name('tr')]
        assert rows == ['Name\nValue', 'key value']
    _test_export(
        element_tester,
        object_export_fn,
        lambda _: state['element'].send_keys('AAE'),
        find_exported,
        lambda _: None,
        verify_object_modal
    )


def _test_export(element_tester, export_fn, *fns):
    element_class = 'element1'

    def builder(page):
        page._exporter.export_fn = export_fn
        page.new_text('hello world')
        page.new_input(props={'className': element_class})

    def finder(driver):
        state['body'] = driver.find_element_by_tag_name('body')
        state['element'] = driver.find_element_by_class_name(element_class)
        state['options_button'] = driver.find_element_by_class_name('ant-btn-icon-only')
        state['element'].click()

    state.clear()

    if export_fn is download_export_fn:
        fns = list(fns) + [find_exported]

    element_tester(builder, finder, *fns)


def wait_for_options_modal(driver):
    assert 'hidden' in state['body'].get_attribute('style')
    state['button'] = driver.find_element_by_class_name('ant-btn-primary')
    state['button'].send_keys('1' * 100)
    time.sleep(1)


def find_exported(driver):
    assert 'hello world' in state['html']


def download_export_fn(index_html):
    state['html'] = index_html
    return index_html


def object_export_fn(index_html):
    state['html'] = index_html
    return {'key': 'value'}
