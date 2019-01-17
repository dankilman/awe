import random

from awe import Page


def main():
    page = Page()
    b = page.element_builder
    page.new('h1').new_text('Simple Report')
    page.new_text('''Things weren't always so good for Foxy Fox.
                     There were days when Fox had to do {thing}, which was hard and not very satisfying.
    '''.format(thing='documentation'))
    page.new('div').s.new_inline('But things are ').n.new('em').new_inline('better').n.new_inline(' now.')
    page.new_text()
    table = page.new_table(['Day', 'Number Of Emotions'])
    for i in range(5):
        number = random.randint(0, 1000)
        url = 'https://www.google.com/search?q={}'.format(number)
        table.append([
            'Day {}'.format(i),
            b.link(url).s.new('em').new_inline(str(number)).n.new_inline(' Emotions')
        ])
    page.start(block=True)


if __name__ == '__main__':
    main()
