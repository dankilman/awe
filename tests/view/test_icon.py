from ..infra import element_tester, driver, page


def test_icon(element_tester):
    icon1_class = 'icon1'
    icon2_class = 'icon2'
    icon3_class = 'icon3'
    icon4_class = 'icon4'

    def builder(page):
        page.new_icon('up-circle', props={'className': icon1_class})
        page.new_icon('up-circle', theme='filled', props={'className': icon2_class})
        page.new_icon('up-circle', spin=True, props={'className': icon3_class})
        page.new_icon('up-circle', theme='twoTone', two_tone_color='red', props={'className': icon4_class})

    def finder(driver):
        icon1 = driver.find_element_by_class_name(icon1_class)
        icon2 = driver.find_element_by_class_name(icon2_class)
        icon3 = driver.find_element_by_class_name(icon3_class)
        icon4 = driver.find_element_by_class_name(icon4_class)
        for icon in [icon1, icon2, icon3, icon4]:
            assert 'anticon-up-circle' in icon.get_attribute('class')
        # outlined
        assert len(icon1.find_elements_by_tag_name('path')) == 2
        # filled
        assert len(icon2.find_elements_by_tag_name('path')) == 1
        assert 'anticon-spin' in icon3.find_element_by_tag_name('svg').get_attribute('class')
        icon4_paths = [e.get_attribute('fill') for e in icon4.find_elements_by_tag_name('path')]
        assert 'red' in icon4_paths

    element_tester(builder, finder)
