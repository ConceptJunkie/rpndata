#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnPersistence.py
# //
# //  RPN command-line calculator factoring utilities
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import six

if six.PY3:
    from functools import lru_cache
else:
    from pylru import lrudecorator as lru_cache
    FileNotFoundError = IOError

import os
import sqlite3

from rpn.rpnUtils import getSourcePath, getUserDataPath

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  getCacheFileName
# //
# //******************************************************************************

@lru_cache( 10 )
def getCacheFileName( name ):
    return getUserDataPath( ) + os.sep + name + '.cache'


# //******************************************************************************
# //
# //  getPrimeCacheFileName
# //
# //******************************************************************************

@lru_cache( 10 )
def getPrimeCacheFileName( name ):
    return getDataPath( ) + os.sep + name + '.cache'


# //******************************************************************************
# //
# //  deleteCache
# //
# //******************************************************************************

def deleteCache( name ):
    if doesCacheExist( name ):
        os.remove( getCacheFileName( name ) )


# //******************************************************************************
# //
# //  saveToCache
# //
# //******************************************************************************

def saveToCache( db, cursor, key, value, commit=True ):
    cursor.execute( '''INSERT INTO cache( id, value ) VALUES( ?, ? )''', ( key, value ) )

    if commit:
        db.commit( )


# //******************************************************************************
# //
# //  doesCacheExist
# //
# //******************************************************************************

def doesCacheExist( name ):
    return os.path.isfile( getCacheFileName( name ) )


# //******************************************************************************
# //
# //  createPrimeCache
# //
# //******************************************************************************

def createPrimeCache( name ):
    db = sqlite3.connect( getCacheFileName( name ) )

    cursor = db.cursor( )
    cursor.execute( '''CREATE TABLE cache( id INTEGER PRIMARY KEY, value INTEGER )''' )
    db.commit( )

    return db, cursor


# //******************************************************************************
# //
# //  openPrimeCache
# //
# //******************************************************************************

def openPrimeCache( name ):
    if name in g.cursors:
        return g.cursors[ name ]
    else:
        try:
            g.databases[ name ] = sqlite3.connect( getPrimeCacheFileName( name ) )
            g.cursors[ name ] = g.databases[ name ].cursor( )
        except:
            raise ValueError( 'prime number table ' + name + ' can\'t be found.  Run "prepareRPNPrimeData" to create the prime data.' )

