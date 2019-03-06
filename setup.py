#!/usr/bin/env python

# //******************************************************************************
# //
# //  setup.py
# //
# //  RPN command-line calculator data generator, setup script for the
# //  rpnChiladaData wheel
# //
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

requirements = 'requirements.txt'
rpndata = 'rpndata'

import os
import glob

from setuptools import setup, find_packages
from rpn.rpnVersion import PROGRAM_VERSION

import rpn.rpnGlobals as g

def read( *paths ):
    '''Build a file path from *paths* and return the contents.'''
    with open( os.path.join( *paths ), 'r' ) as f:
        return f.read( )

setup(
    name = 'rpnChiladaData',
    version = PROGRAM_VERSION,
    description = 'command-line RPN calculator data files',
    long_description =
'''
rpnChilada is a command-line Reverse-Polish Notation calculator that was
first written in C in 1988 as a four-function calculator.

rpnChiladaData is the package containing the data files for rpnChilada that
rarely change.
''',

    url = 'http://github.com/ConceptJunkie/rpn/',
    license = 'GPL3',
    author = 'Rick Gutleber',
    author_email = 'rickg@his.com',

    install_requires = open( requirements ).read( ).splitlines( ),

    include_package_data = True,

    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Environment :: Console',
    ],

    packages = find_packages( ),
    #packages = [ ],
    #py_modules = [ ],

    # This maps the directories to the installed location under site-packages/
    package_dir = { '.' : 'rpn' },

    entry_points = {
    }
)

