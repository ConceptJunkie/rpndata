#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnVersion.py
# //
# //  rpnChiladaData version identification
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

# //******************************************************************************
# //
# //  version variable initialization
# //
# //******************************************************************************

PROGRAM_NAME = 'rpnChiladaData'
PROGRAM_VERSION = '1.1.0'
PROGRAM_VERSION_NAME = '1.1.0'
COPYRIGHT_MESSAGE = 'copyright (c) 2019, Rick Gutleber (rickg@his.com)'

if PROGRAM_VERSION != PROGRAM_VERSION_NAME:
    PROGRAM_VERSION_STRING = ' ' + PROGRAM_VERSION + ' (' + PROGRAM_VERSION_NAME + ')'
else:
    PROGRAM_VERSION_STRING = ' ' + PROGRAM_VERSION

RPN_PROGRAM_NAME = PROGRAM_NAME + PROGRAM_VERSION_STRING

PROGRAM_DESCRIPTION = 'RPN command-line calculator prime number data generator'

