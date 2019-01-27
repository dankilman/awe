import random
import time


from awe import Page


def updater(card):
    while True:
        card.text = 'Got {}'.format(random.randint(1, 100))
        time.sleep(0.1 + random.random())


def main():
    page = Page()
    grid = page.new_grid(columns=3)
    for _ in range(3):
        grid.new_card(updater=updater)
    page.start(block=True)


if __name__ == '__main__':
    main()
