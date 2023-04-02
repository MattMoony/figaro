# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

BPATH: str = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(BPATH, 'README.md'), 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION: str = f.read()

def version() -> str:
    from figaro.__version__ import version
    return version

setup(
    name='figaro',
    version=version(),
    author='m4ttm00ny',
    author_email='m4ttm00ny@gmail.com',
    description=(
        'Real-time open-source voice modification program & sound board. Can be useful for many things, especially when used in combination with virtual sound i/o devices.',
    ),
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/MattMoony/figaro',
    project_urls={
        'Homepage': 'https://github.com/MattMoony/figaro',
        'Documentation': 'https://m4ttm00ny.xyz/figaro',
        'Source': 'https://github.com/MattMoony/figaro',
        'Tracker': 'https://github.com/MattMoony/figaro/issues',
    },
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
    ],
    packages=[
        'figaro',
    ],
    entry_points={
        'console_scripts': [
            'figaro = figaro.cli:main',
        ],
    },
    package_data={
    },
    install_requires=[
        'asciimatics',
        'colorama',
        'jwt',
        'numpy',
        'pash-cmd',
        'Pillow',
        'PyAudio',
        'pydub',
        'pycryptodome',
        'pynput',
        'qrcode',
        'websockets',
        'Yapsy',
    ],
)