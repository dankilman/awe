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
