import time

from awe import Page


def raise_error():
    raise RuntimeError('Sit down, this is bad.')


def export_fn(index_html):
    time.sleep(1)
    raise_error()
    return index_html


def main():
    page = Page(export_fn=export_fn)
    page.new_button(raise_error)
    page.start(block=True)


if __name__ == '__main__':
    main()
