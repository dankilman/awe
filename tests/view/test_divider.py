from ..infra import driver, page, retry

DIVIDER_CLASS = 'ant-divider'


def test_divider(driver, page):
    @retry()
    def find_divider():
        driver.get('http://localhost:{}'.format(page._port))
        driver.find_element_by_class_name(DIVIDER_CLASS)
    page.new_divider()
    page.start(open_browser=False)
    find_divider()
