from awe import Page


def main():
    page = Page()
    collapse = page.new_collapse()
    panel1 = collapse.new_panel('Panel 1', active=True)
    panel1.new_text('Hello From Panel 1')
    panel2 = collapse.new_panel(active=False)
    panel2.header.new_icon('pie-chart')
    panel2.header.new_inline(' Panel 2')
    panel2.new_text('Hello From Panel2')
    panel3 = collapse.new_panel('Panel 3')
    panel3.new_text('Hello From Panel3')
    page.start(block=True)


if __name__ == '__main__':
    main()
