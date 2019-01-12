from awe import Page, CustomElement


class Popover(CustomElement):

    def _init(self, title):
        self.update_props({'title': title})

    @classmethod
    def _js(cls):
        return '''
        register((popover) => (
            <antd.Popover {...popover.props}>
                {popover.children}
            </antd.Popover>
        ));
        '''


def main():
    page = Page()
    popover = page.new(Popover, title='Some Title')
    popover.new_button(lambda: None, 'Hover Me!')
    content = popover.new_prop('content')
    content.new_text('line 1')
    content.new_text('line 2')
    page.start(block=True)


if __name__ == '__main__':
    main()
