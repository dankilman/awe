import sys
import os
import tempfile
import time

from awe import Page


def export_fn(index_html):
    filename = 'offline-export-{}.html'.format(time.time())
    output_path = os.path.join(tempfile.gettempdir(), filename)
    with open(output_path, 'w') as f:
        f.write(index_html)
    return {'path': output_path}


def main():
    page = Page(offline=True, export_fn=export_fn)
    page.new_text('Hello')
    sys.stdout.write(page.export()['path'])


if __name__ == '__main__':
    main()
