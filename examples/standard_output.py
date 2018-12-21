import time

from pages import Page


def main():
    page = Page()
    page.start()
    page.new_text('Header', style={'fontSize': '1.5em', 'color': '#ff0000'})
    for i in range(20):
        page.new_text('{} hello {}'.format(i, i), style={'color': 'blue'})
        time.sleep(0.1)
    page.block()


if __name__ == '__main__':
    main()
