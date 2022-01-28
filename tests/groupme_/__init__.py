#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import functools

import utilatest

import groupme.cli

#pylint: disable=invalid-name
run = functools.partial(
    utilatest.run_command,
    main=groupme.cli.main,
    process=groupme.cli.PROCESS,
    success=True,
)
fail = functools.partial(
    utilatest.run_command,
    main=groupme.cli.main,
    process=groupme.cli.PROCESS,
    success=False,
)
