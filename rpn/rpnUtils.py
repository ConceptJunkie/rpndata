#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnUtils.py
# //
# //  rpnChilada utility functions
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import functools
import itertools
import os
import sys

from functools import lru_cache, reduce
from mpmath import arange, fadd, floor, im, log10, mag, mp, mpmathify, nint, \
                   nstr, workdps

from rpn.rpnDebug import debugPrint
from rpn.rpnGenerator import RPNGenerator

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


# //******************************************************************************
# //
# //  removeUnderscores
# //
# //******************************************************************************

def removeUnderscores( source ):
    '''This function replaces the underscores in a string with spaces, and is
    used for formatting unit output.'''
    result = ''

    for c in source:
        if c == '_':
            result += ' '
        else:
            result += c

    return result


# //******************************************************************************
# //
# //  addAliases
# //
# //******************************************************************************

def addAliases( operatorList, aliases ):
    '''Adds the predefined aliases from the operator table into the global alias list.'''
    for index, operator in enumerate( operatorList ):
        aliasList = [ key for key in aliases if operator == aliases[ key ] ]

        if operator in g.unitOperators:
            unitInfo = g.unitOperators[ operator ]

            if unitInfo.abbrev != '':
                aliasList.append( unitInfo.abbrev )

            aliasList.extend( unitInfo.aliases )

            aliasList = list( set( aliasList ) )

        if aliasList:
            operatorList[ index ] += ' (' + ', '.join( sorted( aliasList ) ) + ')'


# //******************************************************************************
# //
# //  validateOptions
# //
# //******************************************************************************

def validateOptions( args ):
    '''Validates arguments for options that take arguments, and also checks for
    options that are mutually exclusive.'''
    if args.hex:
        if args.output_radix != 10 and args.output_radix != 16:
            return False, '-r and -x can\'t be used together'

        if args.octal:
            return False, '-x and -o can\'t be used together'

    if args.octal:
        if args.output_radix != 10 and args.output_radix != 8:
            return False, '-r and -o can\'t be used together'

    if args.comma and args.integer_grouping > 0 :
        return False, 'rpn:  -c can\'t be used with -i'

    return True, ''


# //******************************************************************************
# //
# //  validateArguments
# //
# //******************************************************************************

def validateArguments( terms ):
    '''Does some preliminary argument validatation, such as checking fo matching
    braces and braces.'''
    bracketCount = 0

    for term in terms:
        if term == '[':
            bracketCount += 1
        elif term == ']':
            bracketCount -= 1

    if bracketCount:
        print( 'rpn:  mismatched brackets (count: {})'.format( bracketCount ) )
        return False

    parenCount = 0

    for term in terms:
        if term == '(':
            parenCount += 1
        elif term == ')':
            parenCount -= 1

    if parenCount:
        print( 'rpn:  mismatched parenthesis (count: {})'.format( parenCount ) )
        return False

    braceCount = 0

    for term in terms:
        if term == '{':
            braceCount += 1
        elif term == '}':
            braceCount -= 1

    if braceCount:
        print( 'rpn:  mismatched braces (count: {})'.format( braceCount ) )
        return False

    return True


# //******************************************************************************
# //
# //  getCurrentArgList
# //
# //******************************************************************************

def getCurrentArgList( valueList ):
    argList = valueList

    for i in range( 0, g.nestedListLevel ):
        argList = argList[ -1 ]

    return argList


# //******************************************************************************
# //
# //  abortArgsNeeded
# //
# //******************************************************************************

def abortArgsNeeded( term, index, argsNeeded ):
    '''Issues the error message when an operator is provided with an insufficient
    number of arguments.'''
    print( 'rpn:  error in arg ' + format( index ) + ':  operator \'' + term + '\' requires ' +
           format( argsNeeded ) + ' argument', end = '' )

    print( 's' if argsNeeded > 1 else '' )


# //******************************************************************************
# //
# //  getExpandedFactorList
# //
# //******************************************************************************

def getExpandedFactorList( factors ):
    '''Takes a list of tuples where each tuple is a prime factor and an exponent
    and returns a simple list of prime factors.'''
    factorMap = map( lambda x: [ x[ 0 ] ] * x[ 1 ], factors )
    return sorted( reduce( lambda x, y: x + y, factorMap, [ ] ) )


# //******************************************************************************
# //
# //  real
# //
# //  Skipping the standard naming convention to keep this name really short.
# //
# //******************************************************************************

def real( n ):
    '''Validates that a value is real and throws an error if it isn't.'''
    if isinstance( n, ( list, RPNGenerator ) ):
        return n

    if im( n ) != 0:
        raise ValueError( 'real argument expected ({})'.format( n ) )

    return n


# //******************************************************************************
# //
# //  real_int
# //
# //  Skipping the standard naming convention to keep this name really short.
# //
# //******************************************************************************

def real_int( n ):
    '''Validates that a value is a real integer and throws an error if it
    isn't.'''
    if im( n ) != 0:
        raise ValueError( 'real argument expected ({})'.format( n ) )

    if n != floor( n ):
        raise ValueError( 'integer argument expected ({})'.format( n ) )

    return int( n )


# //******************************************************************************
# //
# //  getMPFIntegerAsString
# //
# //******************************************************************************

def getMPFIntegerAsString( n ):
    '''Turns an mpmath mpf integer value into a string for use by lexicographic
    operators.'''
    if n == 0:
        return '0'
    else:
        return nstr( nint( n ), int( floor( log10( n ) + 10  ) ) )[ : -2 ]


# //******************************************************************************
# //
# //  addEchoArgument
# //
# //******************************************************************************

def addEchoArgument( argument ):
    '''Echos the argument in the rpn output while continuing to use it for
    evaluation.'''
    if isinstance( argument, list ) and len( argument ) == 1:
        g.echoArguments.append( argument[ 0 ] )
    else:
        g.echoArguments.append( argument )

    return argument


# //******************************************************************************
# //
# //  parseNumerals
# //
# //******************************************************************************

def parseNumerals( argument ):
    '''
    '-' is a special character that defines a range from the preceding character
    to the succeeding character.

    Therefore, '-' is not a valid numeral, but really, who would want to do that?
    '''
    result = ''

    previous = ''
    makeRange = False

    for c in argument:
        if c == '-':
            makeRange = True

            if previous == '':
                raise ValueError( 'invalid numeral expression' )
        else:
            if makeRange:

                for c2 in range( ord( previous ) + 1, ord( c ) + 1 ):
                    result += chr( c2 )

                makeRange = False
            else:
                result += c

            previous = c

    if makeRange:
        raise ValueError( 'invalid numeral expression' )

    return result


# //******************************************************************************
# //
# //  oneArgFunctionEvaluator
# //
# //******************************************************************************

def oneArgFunctionEvaluator( ):
    def oneArgFunction( func ):
        @functools.wraps( func )

        def evaluateOneArg( arg ):
            if isinstance( arg, list ):
                result = [ evaluateOneArg( i ) for i in arg ]
            elif isinstance( arg, RPNGenerator ):
                result = RPNGenerator.createChained( arg.getGenerator( ), func )
            else:
                result = func( arg )

            return result

        return evaluateOneArg

    return oneArgFunction


# //******************************************************************************
# //
# //  listArgFunctionEvaluator
# //
# //******************************************************************************

def listArgFunctionEvaluator( ):
    def listArgFunction( func ):
        @functools.wraps( func )

        def evaluateList( arg ):
            if isinstance( arg, ( list, RPNGenerator ) ):
                result = func( arg )
            else:
                result = func( [ arg ] )

            return result

        return evaluateList

    return listArgFunction


# //******************************************************************************
# //
# //  listAndOneArgFunctionEvaluator
# //
# //******************************************************************************

def listAndOneArgFunctionEvaluator( ):
    def listAndOneArgFunction( func ):
        @functools.wraps( func )

        def evaluateListAndOneArg( arg1, arg2 ):
            if isinstance( arg2, list ):
                result = [ evaluateListAndOneArg( arg1, i ) for i in arg2 ]
            elif isinstance( arg2, RPNGenerator ):
                result = RPNGenerator.createChained( arg.getGenerator( ), func )
            else:
                result = func( arg1, arg2 )

            return result

        return evaluateListAndOneArg

    return listAndOneArgFunction


# //******************************************************************************
# //
# //  twoArgFunctionEvaluator
# //
# //******************************************************************************

def twoArgFunctionEvaluator( ):
    def twoArgFunction( func ):
        @functools.wraps( func )

        def evaluateTwoArgs( _arg1, _arg2 ):
            if isinstance( _arg1, list ):
                len1 = len( _arg1 )

                if len1 == 1:
                    arg1 = _arg1[ 0 ]
                    list1 = False
                else:
                    arg1 = _arg1
                    list1 = True

                generator1 = False
            else:
                arg1 = _arg1
                list1 = False

            generator1 = isinstance( arg1, RPNGenerator )

            if isinstance( _arg2, list ):
                len2 = len( _arg2 )

                if len2 == 1:
                    arg2 = _arg2[ 0 ]
                    list2 = False
                else:
                    arg2 = _arg2
                    list2 = True

                generator2 = False
            else:
                arg2 = _arg2
                list2 = False

            generator2 = isinstance( arg2, RPNGenerator )

            if generator1:
                if generator2:
                    iter1 = iter( arg1 )
                    iter2 = iter( arg2 )

                    result = [ ]

                    while True:
                        try:
                            i1 = iter1.__next__( )
                            i2 = iter2.__next__( )

                            result.append( func( i1, i2 ) )
                        except:
                            break
                else:
                    result = [ evaluateTwoArgs( i, arg2 ) for i in arg1.getGenerator( ) ]
            elif generator2:
                result = [ evaluateTwoArgs( arg1, i ) for i in arg2.getGenerator( ) ]
            elif list1:
                if list2:
                    result = [ evaluateTwoArgs( arg1[ index ], arg2[ index ] ) for index in range( 0, min( len1, len2 ) ) ]
                else:
                    result = [ evaluateTwoArgs( i, arg2 ) for i in arg1 ]

            else:
                if list2:
                    result = [ evaluateTwoArgs( arg1, j ) for j in arg2 ]
                else:
                    result = func( arg1, arg2 )

            return result

        return evaluateTwoArgs

    return twoArgFunction


# //******************************************************************************
# //
# //  listAndOneArgFunctionEvaluator
# //
# //******************************************************************************

def listAndOneArgFunctionEvaluator( ):
    def listAndOneArgFunction( func ):
        @functools.wraps( func )

        def evaluateListAndOneArg( _arg1, _arg2 ):
            if isinstance( _arg1, list ):
                if isinstance( _arg1[ 0 ], list ):
                    return [ evaluateListAndOneArg( i, _arg2 ) for i in _arg1 ]
                else:
                    arg1 = _arg1
            else:
                arg1 = [ _arg1 ]

            if isinstance( _arg2, list ):
                len1 = len( _arg2 )

                if len1 == 1:
                    arg2 = _arg2[ 0 ]
                    list1 = False
                else:
                    arg2 = _arg2
                    list1 = True

                generator1 = False
            else:
                arg2 = _arg2
                list1 = False

            generator1 = isinstance( arg2, RPNGenerator )

            if generator1:
                iter1 = iter( arg2 )

                result = [ ]

                while True:
                    try:
                        i1 = iter1.__next__( )
                        result.append( func( arg1, i1 ) )
                    except:
                        break
                else:
                    result = [ evaluateListAndOneArg( arg1, i ) for i in arg2.getGenerator( ) ]
            elif list1:
                result = [ evaluateListAndOneArg( arg1, i ) for i in arg2 ]
            else:
                result = func( arg1, arg2 )

            return result

        return evaluateListAndOneArg

    return listAndOneArgFunction



# //******************************************************************************
# //
# //  listAndTwoArgFunctionEvaluator
# //
# //******************************************************************************

def listAndTwoArgFunctionEvaluator( ):
    def listAndTwoArgFunction( func ):
        @functools.wraps( func )

        def evaluateListAndTwoArgs( _arg1, _arg2, _arg3 ):
            if isinstance( _arg1, list ):
                if isinstance( _arg1[ 0 ], list ):
                    return [ evaluateListAndTwoArgs( i, _arg2, _arg3 ) for i in _arg1 ]
                else:
                    arg1 = _arg1
            else:
                arg1 = [ _arg1 ]

            if isinstance( _arg2, list ):
                len1 = len( _arg2 )

                if len1 == 1:
                    arg2 = _arg2[ 0 ]
                    list1 = False
                else:
                    arg2 = _arg2
                    list1 = True

                generator1 = False
            else:
                arg2 = _arg2
                list1 = False

            generator1 = isinstance( arg2, RPNGenerator )

            if isinstance( _arg3, list ):
                len2 = len( _arg3 )

                if len2 == 1:
                    arg3 = _arg3[ 0 ]
                    list2 = False
                else:
                    arg3 = _arg3
                    list2 = True

                generator2 = False
            else:
                arg3 = _arg3
                list2 = False

            generator2 = isinstance( arg3, RPNGenerator )

            if generator1:
                if generator2:
                    iter1 = iter( arg2 )
                    iter2 = iter( arg3 )

                    result = [ ]

                    while True:
                        try:
                            i1 = iter1.__next__( )
                            i2 = iter2.__next__( )

                            result.append( func( arg1, i1, i2 ) )
                        except:
                            break
                else:
                    result = [ evaluateListAndTwoArgs( arg1, i, arg3 ) for i in arg2.getGenerator( ) ]
            elif generator2:
                result = [ evaluateListAndTwoArgs( arg1, arg2, i ) for i in arg3.getGenerator( ) ]
            elif list1:
                if list2:
                    result = [ evaluateListAndTwoArgs( arg1, arg2[ index ], arg3[ index ] ) for index in range( 0, min( len1, len2 ) ) ]
                else:
                    result = [ evaluateListAndTwoArgs( arg1, i, arg3 ) for i in arg2 ]

            else:
                if list2:
                    result = [ evaluateListAndTwoArgs( arg1, arg2, j ) for j in arg3 ]
                else:
                    result = func( arg1, arg2, arg3 )

            return result

        return evaluateListAndTwoArgs

    return listAndTwoArgFunction


# //******************************************************************************
# //
# //  timeout
# //
# //******************************************************************************

class TimeoutError( Exception ):
    pass

def timeout( seconds, error_message = 'Function call timed out' ):
    import signal
    import functools

    def decorated( func ):
        def _handle_timeout( signum, frame ):
            raise TimeoutError( error_message )

        def wrapper( *args, **kwargs ):
            signal.signal( signal.SIGALRM, _handle_timeout )
            signal.alarm( seconds )

            try:
                result = func( *args, **kwargs )
            finally:
                signal.alarm( 0 )
            return result

        return functools.wraps( func )( wrapper )

    return decorated


# //******************************************************************************
# //
# //  loadAstronomyData
# //
# //******************************************************************************

def loadAstronomyData( ):
    if g.astroDataLoaded:
        return

    try:
        from skyfield.api import Loader
        load = Loader( getUserDataPath( ) )

        from skyfield.api import load_file
        from skyfield import api

        g.timescale = load.timescale( )
    except:
        print( "Downloading the astronomy data failed.  Some astronomical functions will not be available.", file=sys.stderr )
        g.astroDataLoaded = True
        g.astroDataAvailable = False
        return

    try:
        g.planets = load( 'de405.bsp' )
        g.ephemeris = load( 'de421.bsp' )
    except:
        print( "Downloading the astronomy data failed.  Some astronomical functions will not be available.", file=sys.stderr )
        g.astroDataLoaded = True
        g.astroDataAvailable = False
        return

    g.astroDataLoaded = True
    g.astroDataAvailable = True

    return True


# //******************************************************************************
# //
# //  matchArgumentTypes
# //
# //******************************************************************************

#TODO

def matchArgumentTypes( args, validArgTypes ):
    result = { }

    for unitTypeList in validArgTypes:
        unitTypes = list( unitTypeList )

        #print( 'unitTypes', unitTypes )

        if len( args ) != len( unitTypes ):
            raise ValueError( 'argument count mismatch in matchArgTypes( )' )

        for arg in args:
            unitType = getWhichArgType( arg, unitTypes )
            #print( 'found unit type', unitType )

            if unitType:
                #print( 'setting unitType', unitType )
                result[ unitType ] = arg
            else:
                result = { }
                #print( 'breaking...' )
                #print( )
                break

            unitTypes.remove( unitType )
        else:
            return result

    #print( 'first loop completed' )
    return None


# //******************************************************************************
# //
# //  getPowerset
# //
# //******************************************************************************

def getPowerset( list ):
    # standard python powerset recipe, minus the empty subset, which is not useful to us
    return itertools.chain.from_iterable( itertools.combinations( list, n ) \
                                                    for n in range( 1, len( list ) + 1 ) )


# //******************************************************************************
# //
# //  flattenList
# //
# //******************************************************************************

def flattenList( list ):
    # standard python list flattening recipe
    return [ item for sublist in list for item in sublist ]


# //******************************************************************************
# //
# //  setAccuracyForN
# //
# //******************************************************************************

def setAccuracyForN( n ):
    magnitude = mag( n )

    if mp.prec < magnitude:
        mp.prec = magnitude



