# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import tests


@utilatest.requires(power.BACHELOR056_PDF)
def test_hefopa(testdir, mp):
    source = power.link(power.BACHELOR056_PDF)
    cmd = f'-i {source} -o {testdir.tmpdir} --hefopa'
    tests.run(cmd, mp=mp)
    outpath = testdir.tmpdir.join('groupme__hefopa_result.yaml')
    merged = serializeraw.load_headerfooter(outpath)
    assert merged
