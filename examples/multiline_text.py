from pages import Page


def main():
    page = Page()
    page.new_text('single line')
    page.new_text()
    page.new_text('line 1\nline 2\nline3\n')
    page.new_text('other single line')
    page.start(block=True)


if __name__ == '__main__':
    main()
