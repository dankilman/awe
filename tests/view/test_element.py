import pytest
from selenium.common.exceptions import NoSuchElementException

from ..infra import element_tester, driver, page


def test_element_style(element_tester):
    element_class = 'element1'
    width = 413

    def builder(page):
        page.new_text(
            text='Some content',
            props={'className': element_class},
            style={'width': width}
        )

    def finder(driver):
        element = driver.find_element_by_class_name(element_class)
        assert element.size['width'] == width

    element_tester(builder, finder)


def test_remove(element_tester):
    text1_class = 'text1'
    text1_text = 'text 1'
    card1_class = 'card1'
    text2_class = 'text2'
    text2_text = 'text 2'
    text3_class = 'text3'
    text3_text = 'text 3'

    state = {}

    def builder(page):
        state['text1'] = page.new_text(text1_text, props={'className': text1_class})
        state['card1'] = page.new_card(props={'className': card1_class})
        state['text2'] = state['card1'].new_text(text2_text, props={'className': text2_class})
        state['text3'] = state['card1'].new_text(text3_text, props={'className': text3_class})

    def finder(driver):
        assert driver.find_element_by_class_name(text1_class).text == text1_text
        assert driver.find_element_by_class_name(card1_class)
        assert driver.find_element_by_class_name(text2_class).text == text2_text
        assert driver.find_element_by_class_name(text3_class).text == text3_text

    def verify_no_elements(class_names):
        def result(driver):
            for class_name in class_names:
                with pytest.raises(NoSuchElementException):
                    driver.find_element_by_class_name(class_name)
        return result

    element_tester(
        builder,
        finder,
        lambda _: state['text1'].remove(),
        verify_no_elements(['text1']),
        lambda _: state['text2'].remove(),
        verify_no_elements(['text2']),
        lambda _: state['card1'].remove(),
        verify_no_elements(['card1', 'text3']),
    )
