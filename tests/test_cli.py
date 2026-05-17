# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utilatest

import tests


def test_run_external_help(mp):
    tests.run('--help', mp=mp)


@pytest.mark.usefixtures('td')
@pytest.mark.parametrize('source', [
    pytest.param(power.ORDER009_PDF, id='order009'),
    pytest.param(power.MASTER072_PDF, id='master072'),
    pytest.param(power.MASTER089_PDF, id='master089'),
    pytest.param(power.DOCU009_PDF, id='docu009'),
    pytest.param(power.DOCU027_PDF, id='docu027'),
    pytest.param(power.DOCU007_PDF, id='docu007'),
])
@utilatest.nightly
def test_run_external(source, mp):
    utilatest.fixture_requires(source)
    source = power.link(source)
    cmd = f'-i {source} -o output'
    tests.run(cmd, mp=mp)


@pytest.mark.usefixtures('td')
@utilatest.nightly
@utilatest.requires(power.BACHELOR056_PDF)
def test_regression_groupmes_problem(mp):
    """There was a problem with not sorted page numbers which leads

    to duplicated header/footer. This was solved by sorting page number
    of left/right page numbers.
    """
    source = power.link(power.BACHELOR056_PDF)
    tests.run(f'-i {source} -j=8', mp=mp)
