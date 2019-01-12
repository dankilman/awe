import datetime

from awe import CustomElement

from ..infra import element_tester, driver, page


def test_custom_element_basic(element_tester):
    custom_class = 'custom1'
    custom_text = 'custom text'

    class TestElement(CustomElement):
        @classmethod
        def _js(cls):
            return 'register((e) => <div {{...e.props}}>{}</div>)'.format(custom_text)

    def builder(page):
        page.new(TestElement, props={'className': custom_class})

    def finder(driver):
        element = driver.find_element_by_class_name(custom_class)
        assert element.tag_name == 'div'
        assert element.text == custom_text

    element_tester(builder, finder)


def test_custom_element_explicit_register(element_tester):
    custom_class = 'custom1'
    custom_text = 'custom text'

    class TestElement(CustomElement):
        @classmethod
        def _js(cls):
            return 'register((e) => <div {{...e.props}}>{}</div>)'.format(custom_text)

    def builder(page):
        page.register(TestElement)
        page.new(TestElement, props={'className': custom_class})

    def finder(driver):
        element = driver.find_element_by_class_name(custom_class)
        assert element.tag_name == 'div'
        assert element.text == custom_text

    element_tester(builder, finder)


def test_custom_element_globals(element_tester):
    custom1_class = 'custom1'
    custom2_class = 'custom2'
    custom3_class = 'custom3'
    custom1_text = 'custom1 text'
    custom2_text = 'custom2 text'
    custom3_text = 'custom3 text'

    class TestElement1(CustomElement):
        @classmethod
        def _js(cls):
            return 'register((e) => <antd.Checkbox {{...e.props}}>{}</antd.Checkbox>)'.format(custom1_text)

    class TestElement2(CustomElement):
        @classmethod
        def _js(cls):
            return '''
            class TestElement2 extends React.Component {
                render() {
                    return <div {...this.props}>custom2 text</div>
                }
            }
            register((e) => <TestElement2 {...e.props} />)
            '''

    class TestElement3(CustomElement):
        @classmethod
        def _js(cls):
            return '''
            class TestElement2 extends Component {
                render() {
                    return <div {...this.props}>custom3 text</div>
                }
            }
            register((e) => <TestElement2 {...e.props} />)
            '''

    def builder(page):
        page.new(TestElement1, props={'className': custom1_class})
        page.new(TestElement2, props={'className': custom2_class})
        page.new(TestElement3, props={'className': custom3_class})

    def finder(driver):
        custom1 = driver.find_element_by_class_name(custom1_class)
        custom2 = driver.find_element_by_class_name(custom2_class)
        custom3 = driver.find_element_by_class_name(custom3_class)
        custom1.find_element_by_class_name('ant-checkbox')
        assert custom1.text == custom1_text
        assert custom2.text == custom2_text
        assert custom3.text == custom3_text

    element_tester(builder, finder)


def test_custom_element_after_page_load(element_tester):
    ref_class = 'ref1'
    custom_class = 'custom1'
    custom_text = 'custom text'

    class TestElement(CustomElement):
        @classmethod
        def _js(cls):
            return 'register((e) => <div {{...e.props}}>{}</div>)'.format(custom_text)

    def builder(page):
        page.new_text('ref', props={'className': ref_class})

    def finder(driver):
        driver.find_element_by_class_name(ref_class)

    def add_custom_element(page):
        page.new(TestElement, props={'className': custom_class})

    def find_custom_element(driver):
        element = driver.find_element_by_class_name(custom_class)
        assert element.tag_name == 'div'
        assert element.text == custom_text

    element_tester(
        builder,
        finder,
        add_custom_element,
        find_custom_element
    )


def test_custom_element_external_script(element_tester):
    custom_class = 'custom1'

    class TestElement(CustomElement):
        _scripts = ['https://unpkg.com/moment@2.23.0/min/moment.min.js']

        @classmethod
        def _js(cls):
            return 'register((e) => <div {...e.props}>{moment().format()}</div>)'

    def builder(page):
        page.new(TestElement, props={'className': custom_class})

    def finder(driver):
        element = driver.find_element_by_class_name(custom_class)
        datetime.datetime.strptime(element.text[:19], '%Y-%m-%dT%H:%M:%S')

    element_tester(builder, finder)
