from os import path
from os.path import dirname

from jinja2 import Environment, FileSystemLoader


def main():
    basedir = path.join(dirname(dirname(__file__)))
    loader = FileSystemLoader(basedir)
    env = Environment(loader=loader)
    load_example = lambda name: loader.get_source(env, 'examples/{}.py'.format(name))[0]
    template = env.get_template('README.jinja.md')
    with open(path.join(basedir, 'README.md'), 'w') as f:
        f.write(template.render(load=load_example))


if __name__ == '__main__':
    main()
