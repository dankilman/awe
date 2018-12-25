import time
import random

from awe import Page


def generate_random_data():
    return [{
        'color': random.choice(['blue', 'yellow']),
        'fruit': random.choice(['apple', 'orange']),
        'temp': random.choice(['cold', 'hot']),
        'city': random.choice(['Tel Aviv', 'New York']),
        'value': random.randint(1, 100)
    }]


def main():
    page = Page()
    data = generate_random_data()
    chart = page.new_chart(data=data, transform={
        'type': 'flat',
        'chart_mapping': ['color', 'fruit'],
        'series_mapping': ['temp', 'city'],
        'value_key': 'value'
    }, moving_window=3 * 60)
    page.start()
    while True:
        time.sleep(0.7)
        chart.add(generate_random_data())


if __name__ == '__main__':
    main()
