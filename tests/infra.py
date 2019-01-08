from __future__ import print_function

import functools
import os
import platform
import pprint
import tempfile
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import awe


@pytest.fixture()
def driver():
    options = Options()
    options.headless = True
    arguments = ['--incognito', '--private']
    if platform.system() == 'Darwin':
        chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        data_dir = os.path.join(tempfile.gettempdir(), 'local-probe-chrome-data')
        options.binary_location = chrome_path
    else:
        arguments.extend(['--no-sandbox', '--disable-dev-shm-usage'])
        data_dir = '/home/circleci/project/data'
    arguments.append('--user-data-dir={}'.format(data_dir))
    for argument in arguments:
        options.add_argument(argument)
    result = webdriver.Chrome(options=options)
    result.set_window_size(1600, 1000)
    yield result
    result.close()


@pytest.fixture()
def page():
    return awe.Page()


def retry(attempts=5, interval=1):
    def partial(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                print('Attempt {}'.format(i+1))
                try:
                    return fn(*args, **kwargs)
                except BaseException:
                    if i >= attempts - 1:
                        raise
                    time.sleep(interval)
        return wrapper
    return partial


def _get_logs(driver):
    logs = driver.get_log('browser')
    return _remove_babel_browser_warning(logs)


@pytest.fixture()
def element_tester(driver, page):
    def tester(builder, finder, *rest):
        logs = None
        builder(page)
        page.start(open_browser=False)
        try:
            def new_finder():
                driver.get('http://localhost:{}'.format(page._port))
                finder(driver)
            retry()(new_finder)()
            assert len(rest) % 2 == 0
            for i in range(0, len(rest), 2):
                current_modifier = rest[i]
                current_finder = rest[i + 1]
                if current_modifier:
                    current_modifier(page)
                retry()(current_finder)(driver)
            logs = _get_logs(driver)
            if getattr(builder, 'validate_logs_exist', False):
                assert logs
            else:
                assert not logs
        finally:
            if not logs:
                logs = _get_logs(driver)
            print('Browser Logs:')
            pprint.pprint(logs)

    return tester


def _remove_babel_browser_warning(logs):
    message = 'You are using the in-browser Babel transformer'
    return [l for l in logs if message not in l['message']]
