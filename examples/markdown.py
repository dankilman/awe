from awe import Page


def main():
    page = Page()
    page.new_markdown('''
# Hello There

This is a markdown document. Thanks react-markdown!

## Let's try a list

1. Item 1
1. Item 2
1. Item 3
    ''')
    page.start(block=True)


if __name__ == '__main__':
    main()
