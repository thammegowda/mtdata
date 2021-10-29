#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/6/20

import re
from pathlib import Path

from setuptools import setup, find_namespace_packages

long_description = Path('README.md').read_text(encoding='utf-8', errors='ignore')

classifiers = [  # copied from https://pypi.org/classifiers/
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Utilities',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: General',
    'Topic :: Text Processing :: Filters',
    'Topic :: Text Processing :: Linguistic',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3 :: Only',
]

init_file = Path(__file__).parent / 'mtdata' / '__init__.py'
init_txt = init_file.read_text()
version_re = re.compile(r'''__version__ = ['"]([0-9.]+(-dev)?)['"]''')
__version__ = version_re.search(init_txt).group(1)
desc_re = re.compile(r'''__description__ = ['"](.*)['"]''')
__description__ = desc_re.search(init_txt).group(1)
assert __version__
assert __description__


setup(
    name='mtdata',
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=classifiers,
    python_requires='>=3.7',
    url='https://github.com/thammegowda/mtdata',
    download_url='https://github.com/thammegowda/mtdata',
    platforms=['any'],
    author='Thamme Gowda',
    author_email='tgowdan@gmail.com',
    packages=find_namespace_packages(exclude=['crawler']),
    keywords=['machine translation', 'datasets', 'NLP', 'natural language processing,'
                                                        'computational linguistics'],
    entry_points={
        'console_scripts': [
            'mtdata=mtdata.__main__:main',
            'mtdata-iso=mtdata.iso.__main__:main',
                            ],
    },
    install_requires=[
        'requests==2.26.0',
        'enlighten==1.10.1',
        'portalocker==2.3.0',
        'pybtex==0.24.0',
        'ruamel.yaml >= 0.17.10',
    ],
    include_package_data=True,
    zip_safe=False,
)
