"""Setup/Installation."""

import io
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Package meta-data.
NAME = 'TEx'
DESCRIPTION = 'Telegram Explorer'
URL = 'https://github.com/guibacellar/TBD HERE/'
AUTHOR = 'Th3 0bservator'
EMAIL = 'th30bservator@gmail.com'
REQUIRES_PYTHON = '>=3.7.6'
VERSION = open('__version__.txt').read()

# What packages are optional?
EXTRAS = {
}

here = os.path.abspath(os.path.dirname(__file__))

REQUIRED = [
    'selenium==3.141.0',
    'beautifulsoup4==4.9.3',
    'pytz==2021.1',
    'urllib3==1.26.3',
    'requests==2.25.1',
    'networkx==2.6.2',
    'bs4==0.0.1',
    'lxml==4.6.3',
    'soupsieve==2.2.1',
    'requests-futures==1.0.0',
    'SQLAlchemy==1.4.22'
]

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README_PYPI.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    keyword=[
        "CyberSecurity",
        "Investigation",
        "OSINT",
        "OpenSourceIntelligence",
        "Tool"
    ],
    packages=['OSIx'],
    package_data={
        'OSIx': ['py.typed'],
    },
    install_requires=REQUIRED,
    setup_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='Apache-2.0',
    classifiers=[
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Security',
        'Topic :: Utilities'
    ],
    project_urls={
        'Bug Tracker': 'https://github.com/guibacellar/TBD HERE/issues',
        'Documentation': 'https://github.com/guibacellar/TBD HERE/blob/develop/README.md',
        'Source Code': 'https://github.com/guibacellar/TBD HERE/'
    }
)
