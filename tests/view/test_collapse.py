from ..infra import element_tester, driver, page


def test_collapse_basic(element_tester):
    collapse_class = 'collapse1'
    panel1_class = 'panel1'
    panel1_text = 'panel 1'
    panel2_class = 'panel2'
    panel2_text = 'panel 2'

    def builder(page):
        collapse = page.new_collapse(props={'className': collapse_class})
        collapse.new_panel(panel1_text, props={'className': panel1_class})
        collapse.new_panel(panel2_text, props={'className': panel2_class})

    def finder(driver):
        collapse = driver.find_element_by_class_name(collapse_class)
        panel1 = collapse.find_element_by_class_name(panel1_class)
        panel2 = collapse.find_element_by_class_name(panel2_class)
        assert 'ant-collapse' in collapse.get_attribute('class')
        for panel in [panel1, panel2]:
            assert 'ant-collapse-item' in panel.get_attribute('class')
        assert panel1.text == panel1_text
        assert panel2.text == panel2_text

    element_tester(builder, finder)


def test_collapse_active(element_tester):
    panel1_class = 'panel1'
    panel2_class = 'panel2'
    panel3_class = 'panel3'
    panel1_inner_text = 'panel 1 inner'
    panel2_inner_text = 'panel 2 inner'
    panel3_inner_text = 'panel 3 inner'

    state = {}

    def builder(page):
        collapse = page.new_collapse()
        collapse.new_panel('h1', active=True, props={'className': panel1_class}).new_text(panel1_inner_text)
        collapse.new_panel('h2', props={'className': panel2_class}).new_text(panel2_inner_text)
        collapse.new_panel('h3', active=True, props={'className': panel3_class}).new_text(panel3_inner_text)

    def finder(driver):
        panel1 = driver.find_element_by_class_name(panel1_class)
        panel2 = driver.find_element_by_class_name(panel2_class)
        panel3 = driver.find_element_by_class_name(panel3_class)
        state.update({
            'panel1': panel1,
            'panel2': panel2,
            'panel3': panel3,
        })
        assert panel1.text == 'h1\n{}'.format(panel1_inner_text)
        assert panel2.text == 'h2'
        assert panel3.text == 'h3\n{}'.format(panel3_inner_text)

    def expand_collapse_panels(page):
        state['panel2'].click()

    def verify_new_state(driver):
        assert state['panel2'].text == 'h2\n{}'.format(panel2_inner_text)

    element_tester(
        builder,
        finder,
        expand_collapse_panels,
        verify_new_state
    )


def test_collapse_panel_prop_header(element_tester):
    collapse_class = 'collapse1'
    panel1_class = 'panel1'
    panel2_class = 'panel2'

    state = {}

    def builder(page):
        collapse = page.new_collapse(props={'className': collapse_class})
        state['collapse'] = collapse
        panel = collapse.new_panel(props={'className': panel1_class})
        panel.header.new_text('line 1')
        panel.header.new_text('line 2')

    def finder(driver):
        panel = driver.find_element_by_class_name(panel1_class)
        assert panel.text == 'line 1\nline 2'

    def add_panel(page):
        panel = state['collapse'].new_panel(props={'className': panel2_class})
        panel.header.new_text('line 3')
        panel.header.new_text('line 4')

    def find_new_panel(driver):
        panel = driver.find_element_by_class_name(panel2_class)
        assert panel.text == 'line 3\nline 4'

    element_tester(
        builder,
        finder,
        add_panel,
        find_new_panel
    )
