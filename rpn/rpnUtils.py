#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnUtils.py
# //
# //  RPN command-line calculator utility functions
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from __future__ import print_function

import six

if six.PY3:
    import builtins
    from functools import lru_cache
else:
    FileNotFoundError = IOError
    from pylru import lrudecorator as lru_cache

import os
import sys

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  getSourcePath
# //
# //******************************************************************************

@lru_cache( 1 )
def getSourcePath( ):
    '''Returns the path for the data files.'''
    if getattr( sys, 'frozen', False ):
        sourcePath = os.path.dirname( sys.executable )
    else:
        sourcePath = os.path.dirname( os.path.realpath( __file__ ) )

    if not os.path.isdir( sourcePath ):
        os.makedirs( sourcePath )

    return sourcePath


# //******************************************************************************
# //
# //  getDataPath
# //
# //******************************************************************************

@lru_cache( 1 )
def getDataPath( ):
    '''Returns the path for the data files.'''
    if getattr( sys, 'frozen', False ):
        dataPath = os.path.dirname( sys.executable )
    else:
        dataPath = os.path.dirname( os.path.realpath( __file__ ) ) + os.sep + g.dataDir

    if not os.path.isdir( dataPath ):
        os.makedirs( dataPath )

    return dataPath


# //******************************************************************************
# //
# //  getUserDataPath
# //
# //******************************************************************************

@lru_cache( 1 )
def getUserDataPath( ):
    '''Returns the path for the cache files.'''
    if os.name == 'nt':
        userDataPath = getDataPath( )
    else:
        userDataPath = os.path.expanduser( '~' ) + os.sep + '.' + g.dataDir

    if not os.path.isdir( userDataPath ):
        os.makedirs( userDataPath )

    return userDataPath


