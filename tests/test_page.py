from awe import Page, CustomElement


def test_export():
    text = 'Hello Test Offline'
    page = Page()
    page.new_text(text)
    assert text in page.export()

    def custom_export_fn(index_html):
        return index_html.upper()

    assert text.upper() in page.export(custom_export_fn)

    page = Page(export_fn=custom_export_fn)
    page.new_text(text)
    assert text.upper() in page.export()


def test_export_with_custom_element():
    js_code = 'register((e) => <div {...e.props}>text</div>)'

    class TestElement(CustomElement):
        @classmethod
        def _js(cls):
            return js_code

    page = Page()
    page.new(TestElement)
    assert js_code in page.export()


def test_offline():
    page = Page(offline=True)
    # shouldn't block
    page.start(block=True)
    page.block()
