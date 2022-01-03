# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila
import utilatest

import tests.groupme_.footerheader.extractor


@utilatest.longrun
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


def test_do_not_merge_pagenumber_footer_bachelor76_page21(testdir, monkeypatch):
    extracted = tests.groupme_.footerheader.extractor.footer(
        power.BACHELOR076_PDF,
        testdir,
        monkeypatch,
        pages=21,
    )
    note = utila.select_page(extracted, 21).footer.notes[0]
    note = note.text.strip()  # TODO: remove strip later
    assert note.endswith('Vgl. Schlick, J. et. al.(2014), S.58f.'), str(note)
