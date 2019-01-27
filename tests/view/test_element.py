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


def test_raw_html_elements(element_tester):
    h1_class = 'h11'
    br_class = 'br1'
    div_class = 'div1'
    div_text = 'div text'

    def builder(page):
        h1 = page.new('h1', props={'className': h1_class})
        h1.new('div', props={'className': div_class}).new_text(div_text)
        h1.new('br', props={'className': br_class})

    def finder(driver):
        h1 = driver.find_element_by_class_name(h1_class)
        assert h1.tag_name == 'h1'
        div = h1.find_element_by_class_name(div_class)
        assert div.tag_name == 'div'
        assert div.text == div_text
        br = h1.find_element_by_class_name(br_class)
        assert br.tag_name == 'br'
    element_tester(builder, finder)


def test_link(element_tester):
    link1_class = 'link1'
    link2_class = 'link2'
    link1_url = 'http://www.example.com'
    link2_url = 'http://www.example2.com'
    text1 = 'text 1'
    text2 = 'text 2'

    def builder(page):
        page.new_link(link1_url, props={'className': link1_class}).new_text(text1)
        page.new_link('something', props={'className': link2_class, 'href': link2_url}).new_text(text2)

    def finder(driver):
        link1 = driver.find_element_by_class_name(link1_class)
        link2 = driver.find_element_by_class_name(link2_class)
        for link in [link1, link2]:
            assert link.tag_name == 'a'
        assert link1.text == text1
        assert link2.text == text2

    element_tester(builder, finder)


def test_dynamic_new_prop(element_tester):
    card_class = 'card1'
    text_class = 'text1'
    title_text = 'Title Text'

    state = {}

    def builder(page):
        state['card'] = page.new_card('text', props={'className': card_class})

    def finder(driver):
        driver.find_element_by_class_name(card_class)

    def add_title(page):
        state['card'].new_prop('title').new_text(title_text, props={'className': text_class})

    def find_title(driver):
        assert driver.find_element_by_class_name(text_class).text == title_text

    element_tester(
        builder,
        finder,
        add_title,
        find_title
    )


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


def test_element_updater(element_tester):
    text1_class = 'text1'
    text2_class = 'text2'
    new_text1 = 'This is the new text'
    new_text2 = 'This is the other new text'

    def builder(page):
        def update_text(text):
            text.text = new_text1
        page.new_text(
            'no_update_yet',
            updater=update_text,
            props={'className': text1_class}
        )

    def finder(driver):
        assert driver.find_element_by_class_name(text1_class).text == new_text1

    def add_updater(page):
        def update_text(text):
            text.text = new_text2
        page.new_text(
            'no_update_yet',
            updater=update_text,
            props={'className': text2_class}
        )

    def verify_updater(driver):
        assert driver.find_element_by_class_name(text2_class).text == new_text2

    element_tester(
        builder,
        finder,
        add_updater,
        verify_updater
    )
