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
import utila

import groupme.footnotes.strategy.parser
import tests.fixtures.footnotes
import tests.footerheader.extractor


@pytest.mark.parametrize('example', [
    pytest.param(tests.fixtures.footnotes.FOOTNOTES,),
    pytest.param(tests.fixtures.footnotes.FOOTNOTES_SECOND,),
])
def test_footer_footenote_parse_notes(example):
    raw, expected_footnotes = example[0], example[1]
    parsed = groupme.footnotes.strategy.parser.parse(raw)
    assert len(parsed) == expected_footnotes


def test_footer_footenote_parse_notes_multiline():
    raw = tests.fixtures.footnotes.FOOTNOTES_SECOND[0]
    parsed = groupme.footnotes.strategy.parser.parse(raw)
    assert len(parsed) == 23, len(parsed)

    assert parsed[0].number == 1
    assert parsed[0].text == ('Aus Grnden der besseren Lesbarkeit wird hier '
                              'und im Folgenden ausschlielich die maskuline '
                              'Form verwendet, wobei immer beide '
                              'Geschlechter gemeint sind.')
    assert parsed[-1].number == 23


def test_footer_master98_page10(testdir, monkeypatch):
    extracted = tests.footerheader.extractor.footer(
        power.MASTER098_PDF,
        testdir,
        monkeypatch,
        pages='10',
    )
    footer_ = utila.select_page(extracted, 10).footer
    notes = footer_.notes
    assert len(notes) == 1
    firstnote_text = notes[0].text.strip()
    # ensure that page number is not merged to note text
    assert firstnote_text.endswith('16)'), firstnote_text
