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
