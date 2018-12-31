from ..infra import element_tester, driver, page


def test_text(element_tester):
    text1 = 'some text'
    text1_new = 'some new text'
    text1_class = 'text1'
    text2 = ''
    text2_class = 'text2'
    text3 = 'some multiline\ntext\nbecause this is what is being tested'
    text3_class = 'text3'
    text4_class = 'text4'

    state = {}

    def builder(page):
        state['text1'] = page.new_text(text1, props={'className': text1_class})
        page.new_text(text2, props={'className': text2_class})
        page.new_text(text3, props={'className': text3_class})
        page.new_text(props={'className': text4_class})

    def finder(driver):
        elements1 = driver.find_elements_by_class_name(text1_class)
        assert len(elements1) == 1
        assert elements1[0].tag_name == 'div'
        assert elements1[0].text == text1
        elements2 = driver.find_elements_by_class_name(text2_class)
        assert len(elements2) == 1
        assert elements2[0].tag_name == 'br'
        elements4 = driver.find_elements_by_class_name(text4_class)
        assert len(elements4) == 1
        assert elements4[0].tag_name == 'br'
        elements3 = driver.find_elements_by_class_name(text3_class)
        assert len(elements3) == 3
        split1, split2, split3 = text3.split('\n')
        element3_1, element3_2, element3_3 = elements3
        for s, e in [(split1, element3_1), (split2, element3_2), (split3, element3_3)]:
            assert e.tag_name == 'div'
            assert e.text == s

    def modifier(page):
        state['text1'].text = text1_new

    def finder2(driver):
        element1 = driver.find_element_by_class_name(text1_class)
        assert element1.text == text1_new

    element_tester(
        builder,
        finder,
        modifier,
        finder2
    )
