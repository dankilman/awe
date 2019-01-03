import os

import pytest

from awe import Page

from ..infra import driver, retry


skip_if_ci = pytest.mark.skipif('os.environ.get("CI")', reason='Sporadic unexplained failures')


@skip_if_ci
def test_page_basic(driver):
    _page(driver, Page())

    @retry()
    def check_page():
        assert driver.title == 'Awe'

    check_page()


@skip_if_ci
def test_page_title(driver):
    title = 'A Custom Page Title'
    _page(driver, Page(title=title))

    @retry()
    def check_page():
        assert driver.title == title

    check_page()


@skip_if_ci
def test_page_width(driver):
    width = 555
    _page(driver, Page(width=width))

    @retry()
    def check_page():
        root = driver.find_element_by_id('root')
        assert root.size['width'] == width

    check_page()


@skip_if_ci
def test_page_style(driver):
    width = 545
    _page(driver, Page(style={'width': width}))

    @retry()
    def check_page():
        root = driver.find_element_by_id('root')
        assert root.size['width'] == width

    check_page()


def _page(driver, page):
    page.start(open_browser=False)
    driver.get('http://localhost:{}'.format(page._port))
