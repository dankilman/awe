from setuptools import setup


setup(
    name='pages',
    version='0.1',
    description='Dynamically updated web based reports/dashboards in python.',
    long_description='',
    license='MIT License',
    author='Dan Kilman',
    packages=['pages'],
    install_requires=[
        'bottle',
        'autobahn[twisted]',
        'twisted',
        'pydash',
        'typing'
    ],
    include_package_data=True,
    zip_safe=False,
)
