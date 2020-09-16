# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila

import tests.groupme_.footerheader.extractor


def test_footer_paper18_page3(testdir, monkeypatch):
    """Regression test to avoid parsing formula as footnote."""
    extracted = tests.groupme_.footerheader.extractor.footer(
        power.PAPER18_PDF,
        testdir,
        monkeypatch,
    )
    page3 = utila.select_page(extracted, 3)
    # do not interpret this formula is footer
    assert not page3.footer
