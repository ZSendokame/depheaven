from setuptools import setup

long_description = open('./README.md')

setup(
    name='dependencyheaven',
    version='1.0.1',
    url='https://github.com/ZSendokame/dependencyheaven',
    license='MIT license',
    author='ZSendokame',
    description='Bored of venvs or manually writing dependencies, specify and get a dependencies file.',
    long_description=long_description.read(),
    long_description_content_type='text/markdown',

    entry_points={
        'console_scripts': [
            'deph=src.main:main'
        ]
    },
)