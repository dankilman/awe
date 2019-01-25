import time

from awe import Page


page_layout = '''
Tabs:
- Tab:
  - [name: Tab 1]
  - Grid:
    - [columns: 3]
    - Table: [[table1, headers: [c 1, c 2, c 3], cols: 2, page_size: 5]]
    - Card:
      - Card: inner
    - Card:
      - Text: [[text1, text: 4 Text]]
      - Text: [[text2, text: 4 Text 2]]
    - Card: [[card1], 0 Time]
    - Card: '6'
    - Card: [[cols: 3], '7']
  - Divider: [[divider1]]
  - Divider
  - Table: [[table2, headers: [c 4, c 5], page_size: 5]]
- Tab:
  - [name: Tab 2]
  - Table: [[table3, headers: [c 6, c 7, c 8], page_size: 5]]
  - Table: [[table4, headers: [c 2, c 5], page_size: 5]]
'''


def run():
    page = Page()
    content = page.new(page_layout)
    ref = content.ref
    page.start()
    for i in range(1000):
        ref.table1.append([i, i ** 2, i ** 3])
        ref.table2.prepend([-i, -i * 12])
        ref.table3.append([-i, -i ** 2, -i ** 3])
        ref.table4.append([i, i * 12])
        ref.text1.text = '4 Text: {}'.format(i * 3)
        ref.text2.text = '4 Text {}'.format(i * 4)
        ref.card1.children[0].text = '{} Time: {}'.format(i, time.time())
        ref.divider1.update_prop('dashed', not ref.divider1.props.get('dashed'))
        time.sleep(5)


def main():
    try:
        run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
