#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from functools import partial

from utilatest import run_command

from groupme.cli import PROCESS
from groupme.cli import main

#pylint: disable=invalid-name
run = partial(run_command, main=main, process=PROCESS, success=True)
fail = partial(run_command, main=main, process=PROCESS, success=False)
