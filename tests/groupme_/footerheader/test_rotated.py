# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila

import tests.groupme_


def test_footer_rotated_master116page102_108(testdir, monkeypatch):
    source = power.link(power.MASTER116_PDF)
    pages = utila.from_tuple((102, 103, 104, 105, 106, 107, 108), separator=',')
    tests.groupme_.run(
        f'-i {source} -o {testdir.tmpdir} --pages {pages} --footer',
        monkeypatch=monkeypatch,
    )
    footerheader = serializeraw.load_headerfooter(testdir.tmpdir)
    header = [item.header for item in footerheader]
    assert len(header) == 7
