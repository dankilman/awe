from ..infra import element_tester, driver, page


def test_divider(element_tester):
    divider_class = 'divider1'

    def builder(page):
        page.new_divider(props={'className': divider_class})

    def finder(driver):
        element = driver.find_element_by_class_name(divider_class)
        assert element.tag_name == 'div'
        assert 'ant-divider' in element.get_attribute('class')

    element_tester(builder, finder)
