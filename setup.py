from setuptools import setup, find_packages

__version__ = '0.0.1'

with open('README.md', 'r') as fh:
    long_description = fh.read()

classifiers = [
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
]

setup(
    name='behave-xray',
    version=__version__,
    packages=find_packages('src'),
    package_dir={"": "src"},
    url='https://github.com/fundakol/behave-xray',
    author='Lukasz Fundakowski',
    author_email='fundakol@yahoo.com',
    description='Behave JIRA XRAY results uploader',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=[
        'behave',
        'requests'
    ],
    keywords='behave JIRA XRAY',
    classifiers=classifiers,
)
