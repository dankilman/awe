from collections import OrderedDict

from ..infra import element_tester, driver, page


def test_table(element_tester):
    headers = ['one', 'two', 'three']
    headers_from_dict = OrderedDict()
    for h in headers:
        headers_from_dict[h] = True
    table1_class = 'table1'
    table2_class = 'table2'
    table3_class = 'table3'
    page_size = 3

    tables = []
    elements = []

    row = lambda n: [n, n*10+n, n*100+n*10+n]

    def builder(page):
        tables.append(page.new_table(headers, props={'className': table1_class}))
        tables.append(page.new_table(headers_from_dict, props={'className': table2_class}))
        tables.append(page.new_table(headers, page_size=page_size, props={'className': table3_class}))

    def base_finder(driver):
        for class_name in [table1_class, table2_class, table3_class]:
            element = driver.find_element_by_class_name(class_name).find_element_by_tag_name('table')
            element_headers = element.find_elements_by_tag_name('th')
            assert len(element_headers) == len(headers)
            th1, th2, th3 = element_headers
            assert [th1.text, th2.text, th3.text] == headers
            elements.append(element)
        assert len(set([id(e) for e in elements])) == 3

    def assert_sequence(sequence):
        for element in elements:
            is_paginated = element is elements[2]
            element_rows = element.find_elements_by_tag_name('tr')
            expected_rows_count = min(page_size, len(sequence)) if is_paginated else len(sequence)
            assert len(element_rows) == expected_rows_count + 1
            expected_texts = [' '.join([str(i) for i in row(n)]) for n in sequence]
            if is_paginated:
                expected_texts = expected_texts[:3]
            actual_texts = [r.text for r in element_rows[1:]]
            assert expected_texts == actual_texts

    def modifier1(page):
        for table in tables:
            for n in [1, 2]:
                table.append(row(n))
            for n in [3, 4]:
                table.prepend(row(n))
            table.extend([row(n) for n in [5, 6, 7]])

    element_tester(
        builder,
        base_finder,
        modifier1,
        lambda _: assert_sequence([4, 3, 1, 2, 5, 6, 7]),
        lambda _: [t.clear() for t in tables],
        lambda _: assert_sequence([]),
        lambda _: [t.set([[1, 11, 111], [2, 22, 222]]) for t in tables],
        lambda _: assert_sequence([1, 2])
    )


def test_element_data(element_tester):
    table_class = 'table1'

    def builder(page):
        b = page.element_builder
        table = page.new_table(['header1', 'header2'], props={'className': table_class})
        table.extend([
            [1, b.link('#').new_text('2')],
            [b.link('#').new_text('3'), 4]
        ])

    def finder(driver):
        element = driver.find_element_by_class_name(table_class).find_element_by_tag_name('table')
        data_rows = element.find_elements_by_tag_name('tr')[1:]
        assert data_rows[0].text == '1\n2'
        assert data_rows[1].text == '3\n4'
        assert data_rows[0].find_element_by_tag_name('a').text == '2'
        assert data_rows[1].find_element_by_tag_name('a').text == '3'

    element_tester(builder, finder)


def test_table_sorting(element_tester):
    table_class = 'table1'
    state = {}

    def builder(page):
        table = page.new_table(['header1', 'header2'], props={'className': table_class})
        table.extend([[5, 'def'], [10, 'hij']])

    def assert_rows(driver, rows):
        table = driver.find_element_by_class_name(table_class).find_element_by_tag_name('table')
        _, data_row1, data_row2 = table.find_elements_by_tag_name('tr')
        assert data_row1.text == rows[0]
        assert data_row2.text == rows[1]

    def finder(driver):
        table = driver.find_element_by_class_name(table_class).find_element_by_tag_name('table')
        rows = table.find_elements_by_tag_name('tr')
        header, data_row1, data_row2 = rows
        header1, header2 = header.find_elements_by_tag_name('th')
        state['header1'] = header1
        state['header2'] = header2
        assert_rows(driver, ['5 def', '10 hij'])

    element_tester(
        builder,
        finder,
        lambda _: [state['header1'].click() for _ in range(2)],
        lambda d: assert_rows(d, ['10 hij', '5 def']),
        lambda _: state['header2'].click(),
        lambda d: assert_rows(d, ['5 def', '10 hij'])
    )
