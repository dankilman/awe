from ..infra import element_tester, driver, page


def test_chart(element_tester):
    chart_class = 'chart1'

    state = {}

    def builder(page):
        chart = page.new_chart(data=[1], transform='numbers', props={'className': chart_class})
        state['chart'] = chart

    def finder(driver):
        driver.find_element_by_class_name(chart_class)

    def add_point(page):
        state['chart'].add([2])

    element_tester(
        builder,
        finder,
        add_point,
        finder
    )
