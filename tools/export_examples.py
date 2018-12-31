from __future__ import print_function

import errno
import importlib
import threading
import os
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


def main():
    try:
        os.makedirs(output_examples_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    os.environ.update({
        'AWE_OFFLINE': '1',
        'AWE_SET_GLOBAL': '1',
    })
    for example, config in examples.items():
        def export_fn(index_html):
            with open(os.path.join(output_examples_dir, '{}.html'.format(example)), 'w') as f:
                f.write(index_html)
        print('Processing {}, {}'.format(example, config))
        module_path = 'examples.{}'.format(example)
        module = importlib.import_module(module_path)
        thread = threading.Thread(target=module.main)
        thread.start()
        terminate_after = config.get('terminate_after')
        if terminate_after:
            time.sleep(terminate_after)
            api.page.close()
        thread.join(timeout=300)
        api.page.export(export_fn=export_fn)


if __name__ == '__main__':
    main()
