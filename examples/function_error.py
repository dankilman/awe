from awe import Page


def raise_error():
    raise RuntimeError('Sit down, this is bad.')


def main():
    page = Page()
    page.new_button(raise_error)
    page.start(block=True)


if __name__ == '__main__':
    main()
