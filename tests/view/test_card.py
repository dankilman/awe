from ..infra import element_tester, driver, page


def test_card(element_tester):
    card1_class = 'card1'
    card2_class = 'card2'
    card1_text = 'card 1'
    card2_text = 'card2'

    def builder(page):
        page.new_card(card1_text, props={'className': card1_class})
        page.new_card(props={'className': card2_class}).new_text(card2_text)

    def finder(driver):
        card1 = driver.find_element_by_class_name(card1_class)
        card2 = driver.find_element_by_class_name(card2_class)
        assert card1.text == card1_text
        assert card2.text == card2_text
        for card in [card1, card2]:
            assert 'ant-card' in card.get_attribute('class')

    element_tester(builder, finder)
