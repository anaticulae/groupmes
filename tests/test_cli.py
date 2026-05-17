# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import utilotest

import tests


def test_run_external_help(mp):
    tests.run('--help', mp=mp)


@pytest.mark.usefixtures('td')
@pytest.mark.parametrize('source', [
    pytest.param(hoverpower.ORDER009_PDF, id='order009'),
    pytest.param(hoverpower.MASTER072_PDF, id='master072'),
    pytest.param(hoverpower.MASTER089_PDF, id='master089'),
    pytest.param(hoverpower.DOCU009_PDF, id='docu009'),
    pytest.param(hoverpower.DOCU027_PDF, id='docu027'),
    pytest.param(hoverpower.DOCU007_PDF, id='docu007'),
])
@utilotest.nightly
def test_run_external(source, mp):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    cmd = f'-i {source} -o output'
    tests.run(cmd, mp=mp)


@pytest.mark.usefixtures('td')
@utilotest.nightly
@utilotest.requires(hoverpower.BACHELOR056_PDF)
def test_regression_groupmes_problem(mp):
    """There was a problem with not sorted page numbers which leads

    to duplicated header/footer. This was solved by sorting page number
    of left/right page numbers.
    """
    source = hoverpower.link(hoverpower.BACHELOR056_PDF)
    tests.run(f'-i {source} -j=8', mp=mp)
