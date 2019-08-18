# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup

version = '0.1.0'

root_dir = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(root_dir, 'README.md'), 'r', encoding='utf-8') as f:
        long_description = f.read()
except IOError:
    long_description = ''

setup(
    name='opf',
    version=version,
    description='flow',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Vladimir Krivopolianskii',
    author_email='krivopolianskii@gmail.com',
    url='',
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    packages=find_packages('src'),
    install_requires=[
        'click',
        'pandas',
        'pyscipopt'
    ],
    entry_points='''
        [console_scripts]
        opf=opf.cli:opf
    ''',
    extras_require={
        'test': [
            'pytest'
        ]
    },
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)