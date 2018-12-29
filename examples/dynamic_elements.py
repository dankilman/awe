import time

from awe import Page


def main():
    page = Page()
    page.start()
    for i in range(3):
        time.sleep(1)
    page.new_text('1')
    page.new_text('2')
    page.block()


if __name__ == '__main__':
    main()
