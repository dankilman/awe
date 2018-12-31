from __future__ import print_function

import errno
import importlib
import os
import threading
import time

from awe import api


output_examples_dir = os.path.join(os.path.dirname(__file__), '../published-examples')

examples = {
    'hello_world': {},
    'button_and_input': {},
    'chart_simple': {
        'terminate_after': 35,
    },
    'chart_complex': {
        'terminate_after': 70,
    },
    'kitchen': {
        'terminate_after': 60,
    },
    'page_properties': {},
    'standard_output': {},
    'collapse': {},
    'chart_flat': {
        'terminate_after': 60,
    }
}


def setup():
    os.environ.update({'AWE_OFFLINE': '1', 'AWE_SET_GLOBAL': '1'})
    try:
        os.makedirs(output_examples_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def main():
    setup()
    for example, config in examples.items():
        print('Processing {}, {}'.format(example, config))
        module = importlib.import_module('examples.{}'.format(example))
        thread = threading.Thread(target=module.main)
        thread.start()
        terminate_after = config.get('terminate_after')
        if terminate_after:
            time.sleep(terminate_after)
            api.page.close()
        thread.join(timeout=300)
        with open(os.path.join(output_examples_dir, '{}.html'.format(example)), 'w') as f:
            f.write(api.page.export())


if __name__ == '__main__':
    main()
