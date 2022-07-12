# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utilatest

import tests


@pytest.mark.parametrize('cmd', [
    ['--help'],
    ['-i', power.link(power.ORDER009_PDF), '-o', 'output'],
    ['-i', power.link(power.MASTER072_PDF), '-o', 'output'],
    ['-i', power.link(power.MASTER089_PDF), '-o', 'output'],
    ['-i', power.link(power.DOCU009_PDF), '-o', 'output'],
    ['-i', power.link(power.DOCU027_PDF), '-o', 'output'],
    ['-i', power.link(power.DOCU007_PDF), '-o', 'output'],
])
@pytest.mark.usefixtures('testdir')
@utilatest.nightly
def test_run_external(cmd, mp):
    """Run help and version and format command to reach basic test coverage"""
    tests.run(cmd, mp=mp)


@pytest.mark.usefixtures('testdir')
@utilatest.nightly
def test_regression_groupme_problem(mp):
    """There was a problem with not sorted page numbers which leads

    to duplicated header/footer. This was solved by sorting page number
    of left/right page numbers.
    """
    source = power.link(power.BACHELOR056_PDF)
    tests.run(f'-i {source} -j=8', mp=mp)
