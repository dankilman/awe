# coding=utf-8
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


def test_custom_element_external_script2(element_tester):
    custom_class = 'custom1'

    class TestElement(CustomElement):
        _scripts = [{'src': 'https://unpkg.com/moment@2.23.0/min/moment.min.js'}]

        @classmethod
        def _js(cls):
            return 'register((e) => <div {...e.props}>{moment().format()}</div>)'

    def builder(page):
        page.new(TestElement, props={'className': custom_class})

    def finder(driver):
        element = driver.find_element_by_class_name(custom_class)
        datetime.datetime.strptime(element.text[:19], '%Y-%m-%dT%H:%M:%S')

    element_tester(builder, finder)


def test_custom_element_external_style(element_tester):
    custom_class = 'custom1'

    class TestElement(CustomElement):
        _styles = ['https://unpkg.com/ionicons@4.2.2/dist/css/ionicons.min.css']

        @classmethod
        def _js(cls):
            return 'register((e) => <div {...e.props}><i className="icon ion-md-heart" /></div>)'

    def builder(page):
        page.new(TestElement, props={'className': custom_class})

    def finder(driver):
        v = driver.execute_script(
            "return window"
            "   .getComputedStyle(document.querySelector('.ion-md-heart'),':before')"
            "   .getPropertyValue('content')"
        )
        assert v == u'""'

    element_tester(builder, finder)


def test_custom_element_external_style2(element_tester):
    custom_class = 'custom1'

    class TestElement(CustomElement):
        _styles = [{'href': 'https://unpkg.com/ionicons@4.2.2/dist/css/ionicons.min.css'}]

        @classmethod
        def _js(cls):
            return 'register((e) => <div {...e.props}><i className="icon ion-md-heart" /></div>)'

    def builder(page):
        page.new(TestElement, props={'className': custom_class})

    def finder(driver):
        v = driver.execute_script(
            "return window"
            "   .getComputedStyle(document.querySelector('.ion-md-heart'),':before')"
            "   .getPropertyValue('content')"
        )
        assert v == u'""'

    element_tester(builder, finder)


def test_custom_element_custom_update_element_action(element_tester):
    custom_class = 'custom1'

    class TestElement(CustomElement):

        def _init(self, data):
            self.update_data(data)

        @classmethod
        def _js(cls):
            return '''
                Awe.registerUpdateElementAction('removeKeys', data => map => map.deleteAll(data));
                register((e) => (
                    <div {...e.props}>
                        {Object.values(e.data.map).map((v, i) => <div key={i.toString()}>{v}</div>)}
                    </div>
                ));
            '''

    element_data = {
        'map': {
            '1': 'one',
            '2': 'two',
            '3': 'three',
            '4': 'four',
        }
    }

    state = {}

    def builder(page):
        state['element'] = page.new(TestElement, data=element_data, props={'className': custom_class})

    def finder(driver):
        element = driver.find_element_by_class_name(custom_class)
        text = element.text
        for v in ['one', 'two', 'three', 'four']:
            assert v in text

    def remove_two_and_four(page):
        element_data['map'].pop('2')
        element_data['map'].pop('4')
        state['element'].update_element(['data', 'map'], action='removeKeys', data=['2', '4'])

    def verify_new_data(driver):
        element = driver.find_element_by_class_name(custom_class)
        text = element.text
        for v in ['one', 'three']:
            assert v in text
        for v in ['two', 'four']:
            assert v not in text

    element_tester(
        builder,
        finder,
        remove_two_and_four,
        verify_new_data
    )
