from awe import Page

from ..infra import driver, retry


def test_page_basic(driver):
    @_retry(driver)
    def check_page():
        assert driver.title == 'Awe'
    check_page()


def test_page_title(driver):
    title = 'A Custom Page Title'

    @_retry(driver, title=title)
    def check_page():
        assert driver.title == title
    check_page()


def test_page_width(driver):
    width = 555

    @_retry(driver, width=width)
    def check_page():
        root = driver.find_element_by_id('root')
        assert root.size['width'] == width
    check_page()


def test_page_style(driver):
    width = 545

    @_retry(driver, style={'width': width})
    def check_page():
        root = driver.find_element_by_id('root')
        assert root.size['width'] == width
    check_page()


def _retry(driver, **page_kwargs):
    def wrapper(fn):
        page = Page(**page_kwargs)
        page.start(open_browser=False)

        @retry()
        def result():
            driver.get('http://localhost:{}'.format(page._port))
            fn()
        return result
    return wrapper
