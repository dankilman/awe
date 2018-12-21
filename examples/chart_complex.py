import time
from random import randint

from pages import Page


def generate_random_data(size):
    level3 = lambda: {'l3_key1': randint(0, 1000), 'l3_key2': randint(0, 1000)}
    level2 = lambda: {'l2_key1': level3(), 'l2_key2': level3(), 'l2_key3': level3()}
    level1 = lambda: {'l1_key1': level2(), 'l1_key2': level2()}
    return [level1() for _ in range(size)]


def main():
    page = Page()
    data = generate_random_data(1)
    chart = page.new_chart(data=data, transform='2to31', moving_window=3 * 60)
    page.start()
    while True:
        time.sleep(5)
        chart.add(generate_random_data(1))


if __name__ == '__main__':
    main()
