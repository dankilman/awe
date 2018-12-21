from random import randint

from awe import Page, inject


@inject(variables=['query'], elements=['table'])
def run_query(query, table):
    rows = []
    try:
        q_from, q_to = query.split(',')
        for i in range(int(q_from), int(q_to) + 1):
            rows.append([i, randint(-i, i), i * i])
    except (ValueError, TypeError):
        rows.append(['invalid query', 'syntax: <from>,<to>', ''])
    table.set(rows)


def main():
    page = Page()
    page.new_input(id='query', on_enter=run_query)
    page.new_table(headers=['one', 'two', 'three'], id='table')
    page.start(block=True)


if __name__ == '__main__':
    main()
