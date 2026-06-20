#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import importlib.metadata
import os

import groupmes.__patch__
import groupmes.path

PACKAGE = 'groupmes'
PROCESS = 'groupme'

__version__ = importlib.metadata.version(PACKAGE)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
