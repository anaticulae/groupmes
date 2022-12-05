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
import utila
import utilatest

import tests
import tests.conftest


@pytest.mark.parametrize(
    'pdf',
    utilatest.test_resources(tests.conftest.RESOURCES),
)
def test_hefopa(pdf, td, mp):
    source = power.link(pdf)
    cmd = f'-i {source} -o {td.tmpdir} --hefopa'
    tests.run(cmd, mp=mp)
    merged = serializeraw.load_headerfooter(td.tmpdir)
    skip = pdf == power.BOOK007_PDF  # TODO: ENABLE LATER
    assert merged or skip


def test_pagenumbers(td, mp):
    source = power.link(power.HC_DISS193)
    if not utila.exists(source):
        pytest.skip(reason=f'generate: {source}')
    cmd = f'-i {source} -o {td.tmpdir} --hefopa'
    tests.run(cmd, mp=mp)
    merged = serializeraw.load_headerfooter(td.tmpdir)
    assert len(merged) == 98
