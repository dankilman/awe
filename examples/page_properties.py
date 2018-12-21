from awe import Page


def main():
    page = Page('Page Properties', width=600, style={
        'backgroundColor': 'red'
    })
    page.new_card('hello')
    page.start(block=True)


if __name__ == '__main__':
    main()
