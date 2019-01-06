from ..infra import element_tester, driver, page


def test_tabs(element_tester):
    tabs_class = 'tabs1'
    tab1_class = 'tab1'
    tab1_name = 'tab 1'
    tab1_inner = 'inner text 1'
    tab2_class = 'tab2'
    tab2_name = 'tab 2'
    tab2_inner = 'inner text 2'

    state = {}

    def builder(page):
        tabs = page.new_tabs(props={'className': tabs_class})
        tabs.new_tab(tab1_name, props={'className': tab1_class}).new_text(tab1_inner)
        tabs.new_tab(tab2_name, props={'className': tab2_class}).new_text(tab2_inner)

    def finder(driver):
        tabs = driver.find_element_by_class_name(tabs_class)
        tabs_headers = tabs.find_elements_by_class_name('ant-tabs-tab')
        assert {tab1_name, tab2_name} == set([t.text for t in tabs_headers])
        tab1 = tabs.find_element_by_class_name(tab1_class)
        tab2 = tabs.find_element_by_class_name(tab2_class)
        state['tab2'] = tab2
        state['tab2_header'] = [t for t in tabs_headers if t.text == tab2_name][0]
        assert tab1.text == tab1_inner
        assert tab2.text == ''

    def click_tab2(page):
        state['tab2_header'].click()

    def verify_change(driver):
        assert state['tab2'].text == tab2_inner

    element_tester(
        builder,
        finder,
        click_tab2,
        verify_change
    )
