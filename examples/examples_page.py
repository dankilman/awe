import os

from awe import Page, CustomElement
import examples


class HighlightJS(CustomElement):

    _scripts = ['https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.14.1/highlight.min.js']
    _styles = ['https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.14.1/styles/tomorrow-night-bright.min.css']

    @classmethod
    def _js(cls):
        return '''
            setTimeout(() => {
                document.querySelectorAll('.python').forEach((block) => {
                    hljs.highlightBlock(block);
                });
            }, 500);
        '''


def main():
    page = Page('Examples', width=900)
    page.register(HighlightJS)
    page.new('h1').new_text('Examples')
    page.new_text('Examples page was created with awe.\n')
    collapse = page.new_collapse()
    for example in examples.examples_order:
        config = examples.exported_examples[example]
        this_dir = os.path.dirname(__file__)
        py_file = os.path.join(this_dir, '{}.py'.format(example))
        md_file = os.path.join(this_dir, '{}.md'.format(example))
        github_link = 'https://github.com/dankilman/awe/blob/master/examples/{}.py'.format(example)
        static_url = 'https://s3.amazonaws.com/awe-static-files/examples/{}.html'.format(example)
        image_url = 'https://s3.amazonaws.com/awe-static-files/examples/{}.{}'.format(example, config['extension'])
        panel = collapse.new_panel('examples/{}.py'.format(example), active=True)
        (panel.new('h2').s
         .new_link(github_link).new_inline('examples/{}.py'.format(example)).n
         .new_inline(' ')
         .new_link(static_url).new_inline(' [static demo]').p)
        with open(md_file) as f:
            panel.new_markdown(f.read())
        panel.new('img', props={'src': image_url}, style={'maxWidth': '100%'})
        panel.new_divider()
        with open(py_file) as f:
            panel.new('pre').new('code').new_inline(
                f.read(),
                style={'borderRadius': '2px'},
                props={'className': 'python'},
            )
    page.start(block=True)


if __name__ == '__main__':
    main()
