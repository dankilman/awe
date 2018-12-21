from pages import Page, inject


@inject(variables=['input1', 'input2'], elements=['button1'])
def do_stuff(input1, input2, button1):
    text = '{} {} {}'.format(button1.count, input1, input2)
    button1.update_data({'text': text})
    button1.count += 1


def main():
    page = Page()
    b = page.new_button(do_stuff, id='button1')
    b.count = 0
    page.new_input(id='input1')
    page.new_input(
        placeholder='Input 2, write anything!',
        on_enter=do_stuff,
        id='input2'
    )
    page.start(block=True)


if __name__ == '__main__':
    main()
