from awe import Page, CustomElement


class Moment(CustomElement):
    _scripts = ['https://unpkg.com/moment@2.23.0/min/moment.min.js']

    @classmethod
    def _js(cls):
        return 'register((e) => <div {...e.props}>{moment().format()}</div>);'


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
    content.new(Moment)
    page.start(block=True)


if __name__ == '__main__':
    main()
