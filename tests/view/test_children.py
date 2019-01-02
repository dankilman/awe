from ..infra import element_tester, driver, page


def test_children(element_tester):

    state = {}

    def builder(page):
        collapse = page.new_collapse(props={'className': 'collapse1'})
        panel1 = collapse.new_panel('panel1', props={'className': 'panel1'}, active=True)
        panel2 = collapse.new_panel('panel2', props={'className': 'panel2'}, active=True)
        panel1.new_text('panel1 text', props={'className': 'panel1-text'})
        panel2.new_text('panel2 text', props={'className': 'panel2-text'})

        grid = page.new_grid(columns=2, props={'className': 'grid1'})
        grid.new_text('grid text1', props={'className': 'grid1-text1'})
        grid.new_text('grid text2', props={'className': 'grid1-text2'})
        grid.new_text('grid text3', props={'className': 'grid1-text3'})
        grid.new_text('grid text4', props={'className': 'grid1-text4'})

        card = page.new_card(props={'className': 'card1'})
        card.new_text('card text1', props={'className': 'card1-text1'})
        card.new_text('card text2', props={'className': 'card1-text2'})

        tabs = page.new_tabs(props={'className': 'tabs1'})
        tab1 = tabs.new_tab('tab1', props={'className': 'tab1'})
        tab2 = tabs.new_tab('tab2', props={'className': 'tab2'})
        tab1.new_text('tab1 text', props={'className': 'tab1-text'})
        tab2.new_text('tab2 text', props={'className': 'tab2-text'})

    def finder(driver):
        find_collapse_children(driver)
        find_grid_children(driver)
        find_card_children(driver)
        find_base_tabs_elements(driver)

    def find_collapse_children(driver):
        ce = driver.find_element_by_class_name('collapse1')
        p1t = ce.find_element_by_class_name('panel1').find_element_by_class_name('panel1-text')
        p2t = ce.find_element_by_class_name('panel2').find_element_by_class_name('panel2-text')
        assert p1t.text == 'panel1 text'
        assert p2t.text == 'panel2 text'

    def find_grid_children(driver):
        def try_find(element, class_name):
            try:
                return element.find_element_by_class_name(class_name)
            except Exception:
                return None
        ges = driver.find_elements_by_class_name('grid1')
        for c in [1, 2, 3, 4]:
            for ge in ges:
                gt = try_find(ge, 'grid1-text{}'.format(c))
                if not gt:
                    continue
                assert gt.text == 'grid text{}'.format(c)
                break
            else:
                raise AssertionError('Not found {}'.format(c))

    def find_card_children(driver):
        ce = driver.find_element_by_class_name('card1')
        p1t = ce.find_element_by_class_name('card1-text1')
        p2t = ce.find_element_by_class_name('card1-text2')
        assert p1t.text == 'card text1'
        assert p2t.text == 'card text2'

    def find_base_tabs_elements(driver):
        state['tabs'] = driver.find_element_by_class_name('tabs1')
        state['inner_tabs'] = state['tabs'].find_elements_by_class_name('ant-tabs-tab')

    def find_tab1_children(driver):
        t1t = state['tabs'].find_element_by_class_name('tab1').find_element_by_class_name('tab1-text')
        assert t1t.text == 'tab1 text'

    def click_tab2(page):
        inner_tab2 = [t for t in state['inner_tabs'] if t.text == 'tab2'][0]
        inner_tab2.click()

    def find_tab2_children(driver):
        t2t = state['tabs'].find_element_by_class_name('tab2').find_element_by_class_name('tab2-text')
        assert t2t.text == 'tab2 text'

    element_tester(
        builder,
        finder,
        None,
        find_tab1_children,
        click_tab2,
        find_tab2_children
    )
