from awe import Page


def main():
    page = Page()
    page.new_text('Hello World!')
    page.start(block=True)


if __name__ == '__main__':
    main()
