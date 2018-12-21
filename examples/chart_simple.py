import time
from random import randint

from awe import Page


def generate_random_data(size, num_series):
    result = []
    for _ in range(size):
        item = []
        for i in range(num_series):
            item.append(randint(i*100, i*100 + 100))
        result.append(item)
    return result


def main():
    args = (1, 3)
    page = Page()
    data = generate_random_data(*args)
    chart = page.new_chart(data=data, transform='numbers')
    page.start()
    while True:
        time.sleep(1)
        chart.add(generate_random_data(*args))


if __name__ == '__main__':
    main()
