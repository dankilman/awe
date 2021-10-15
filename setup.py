import os

from setuptools import setup


os.environ['AWE_BUILD'] = '1'
try:
    from awe import __version__
except ImportError as e:
    raise RuntimeError('Somethings wrong. {}'.format(e))


setup(
    name='awe',
    version=__version__,
    description='Dynamic web based reports/dashboards in python',
    url='https://github.com/dankilman/awe',
    long_description='',
    license='MIT License',
    author='Dan Kilman',
    packages=[
        'awe',
        'awe.resources'
    ],
    install_requires=[
        'six',
        'bottle',
        'autobahn[twisted]',
        'twisted',
        'service_identity',
        'pyyaml<6',
        'txaio',
        'pydash',
        'typing;python_version<"3.7"',
        'requests',
        'click'
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
                'awe = awe.cli:cli'
        ]
    }
)
