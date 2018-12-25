from os import path
from os.path import dirname

from jinja2 import Template


basedir = path.join(dirname(dirname(__file__)))


def load_example(name):
    with open(path.join(basedir, 'examples', '{}.py'.format(name))) as f:
        return f.read()


def load_example_docstring(name):
    with open(path.join(basedir, 'examples', '{}.md'.format(name))) as f:
        return f.read()


def main():
    with open(path.join(basedir, 'README.jinja.md')) as f:
        template_content = f.read()
    template = Template(template_content)
    with open(path.join(basedir, 'README.md'), 'w') as f:
        f.write(template.render(load=load_example,
                                docstring=load_example_docstring))


if __name__ == '__main__':
    main()
