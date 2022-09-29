# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila
import utilatest

import tests


@utilatest.requires(power.MASTER116_PDF)
def test_footer_rotated_master116page102_108(td, mp):
    source = power.link(power.MASTER116_PDF)
    pages = utila.from_tuple((102, 103, 104, 105, 106, 107, 108), separator=',')
    tests.run(
        f'-i {source} -o {td.tmpdir} --pages {pages} --footer',
        mp=mp,
    )
    footerheader = serializeraw.load_headerfooter(td.tmpdir)
    header = [item.header for item in footerheader]
    assert len(header) == 7
