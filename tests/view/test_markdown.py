from ..infra import element_tester, driver, page


def test_markdown(element_tester):
    markdown_class = 'markdown1'
    text = 'Hello There'

    def builder(page):
        page.new_markdown('# {}'.format(text), props={'className': markdown_class})

    def finder(driver):
        element = driver.find_element_by_class_name(markdown_class)
        h1 = element.find_element_by_tag_name('h1')
        assert h1.text == text

    element_tester(builder, finder)
