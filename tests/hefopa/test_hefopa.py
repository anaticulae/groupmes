# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utilatest

import tests
import tests.conftest


@pytest.mark.parametrize(
    'source',
    utilatest.test_resources(tests.conftest.RESOURCES),
)
def test_hefopa(source, testdir, mp):
    source = power.link(power.BACHELOR056_PDF)
    cmd = f'-i {source} -o {testdir.tmpdir} --hefopa'
    tests.run(cmd, mp=mp)
    outpath = testdir.tmpdir.join('groupme__hefopa_result.yaml')
    merged = serializeraw.load_headerfooter(outpath)
    assert merged
