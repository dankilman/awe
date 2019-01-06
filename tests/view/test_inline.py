import pytest
from selenium.common.exceptions import NoSuchElementException

from ..infra import element_tester, driver, page


def test_inline(element_tester):
    inline1_class = 'inline1'
    inline2_class = 'inline2'
    inline3_class = 'inline3'
    inline4_class = 'inline4'
    inline1_text = 'inline 1'
    inline3_text = 'inline 3'
    inline4_text = 'inline 4'

    def builder(page):
        page.new_inline(inline1_text, props={'className': inline1_class})
        inline2 = page.new_inline(props={'className': inline2_class})
        inline2.new_inline(inline3_text, props={'className': inline3_class})
        inline2.new_inline(inline4_text, props={'className': inline4_class})

    def finder(driver):
        inline1 = driver.find_element_by_class_name(inline1_class)
        inline2 = driver.find_element_by_class_name(inline2_class)
        inline3 = inline2.find_element_by_class_name(inline3_class)
        inline4 = inline2.find_element_by_class_name(inline4_class)
        for inline in [inline1, inline2, inline3, inline4]:
            assert inline.tag_name == 'span'
            with pytest.raises(NoSuchElementException):
                inline.find_element_by_tag_name('div')

    element_tester(builder, finder)
