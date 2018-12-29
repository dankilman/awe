import time

from awe import Page


class Kitchen(object):
    def __init__(self, parent):
        self.tabs = parent.new_tabs()
        self.tab1 = Tab1(self.tabs)
        self.tab2 = Tab2(self.tabs)

    def update(self, i):
        self.tab1.update(i)
        self.tab2.update(i)


class Tab1(object):
    def __init__(self, parent):
        self.tab = parent.new_tab('Tab 1')
        self.grid = Grid(self.tab)
        self.divider = self.tab.new_divider()
        self.divider2 = self.tab.new_divider()
        self.table2 = self.tab.new_table(headers=['c 4', 'c 5'], page_size=5)

    def update(self, i):
        self.divider.update_prop('dashed', not self.divider.props.get('dashed'))
        self.table2.prepend([-i, -i * 12])
        self.grid.update(i)


class Grid(object):
    def __init__(self, parent):
        self.grid = parent.new_grid(columns=3)
        self.table1 = self.grid.new_table(headers=['c 1', 'c 2', 'c 3'], cols=2, page_size=5)
        self.cc = self.grid.new_card()
        self.cc_inner = self.cc.new_card('inner')
        self.ct = self.grid.new_card()
        self.t1 = self.ct.new_text('4 Text')
        self.t2 = self.ct.new_text('4 Text 2')
        self.card = self.grid.new_card('0 Time')
        self.card2 = self.grid.new_card('6')
        self.card3 = self.grid.new_card('7', cols=3)

    def update(self, i):
        self.table1.append([i, i ** 2, i ** 3])
        self.card.text = '{} Time: {}'.format(i, time.time())
        self.t1.text = '4 Text: {}'.format(i * 3)
        self.t2.text = '4 Text {}'.format(i * 4)


class Tab2(object):
    def __init__(self, parent):
        self.tab = parent.new_tab('Tab 2')
        self.table3 = self.tab.new_table(headers=['c 6', 'c 7', 'c 8'], page_size=5)
        self.table4 = self.tab.new_table(headers=['c 2', 'c 5'], page_size=5)

    def update(self, i):
        self.table3.append([-i, -i ** 2, -i ** 3])
        self.table4.append([i, i * 12])


def main():
    page = Page()
    kitchen = Kitchen(page)
    page.start()
    try:
        for i in range(1000):
            kitchen.update(i)
            time.sleep(5)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
