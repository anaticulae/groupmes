# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw.path
import power
import pytest
import serializeraw
import utila
import utilatest

import groupme.feature.footer
import groupme.footer.strategy as gfs
import groupme.path
import tests.groupme_
import tests.groupme_.footerheader.extractor


def test_footer_work(testdir):  #pylint:disable=W0621
    root = str(testdir)
    docu27 = power.link(power.DOCU27_PDF)
    dumped = groupme.feature.footer.work(
        iamraw.path.text(docu27),
        iamraw.path.textposition(docu27),
        iamraw.path.fontheader(docu27),
        iamraw.path.fontcontent(docu27),
        iamraw.path.horizontals(docu27),
        iamraw.path.sizeandborder(docu27),
        groupme.path.pagenumbers(docu27),
    )
    assert dumped
    assert len(dumped) > 100, str(dumped)  # there is some content

    utila.file_create(os.path.join(root, 'result.yaml'), dumped)


@pytest.mark.parametrize(
    'strategy, expected_results',
    [
        (gfs.moving.MovingFooterStrategy, 0),
        (gfs.fixed.FixedFooterStrategy, 25),  # TODO: CHECK 25
        (gfs.pages.PageNumberStrategy, 0),
    ])
def test_footer_footerheader_detectionstategy(
        strategy,
        expected_results,
):
    """Check that different strategies work proper with given resources

    TODO: SEE DUPLICATION test_footer_judgement_strategy_quality?"""
    source = power.link(power.DOCU27_PDF)
    horizontals = serializeraw.load_horizontals(source)
    sizeandborders = serializeraw.load_pageborders(source)
    pagenumbers = groupme.path.pagenumbers(source)  # TODO: REMOVE AFTER UPGRADE
    pagenumbers = serializeraw.load_pagenumbers(pagenumbers)
    ptn = serializeraw.create_pagetextnavigators_frompath(source)

    process = strategy(
        horizontals=horizontals,
        sizeandborders=sizeandborders,
        pagenumbers=pagenumbers,
        pagetextnavigators=ptn,
    )
    result = process.result()
    assert len(result) == expected_results, 'not enough footer and header'


@utilatest.skip_longrun
def test_footer_master72_extract(testdir, monkeypatch):
    outdir = testdir.tmpdir
    cmd = f'-i {power.link(power.MASTER072_PDF)}  -o {outdir} --footer --pages=3'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)

    headfoot = serializeraw.load_headerfooter(iamraw.path.headerfooters(outdir))
    footnotes = headfoot[0].footer.notes
    assert len(footnotes) == 6, str(footnotes)

    first = normalize_whitespaces(footnotes[0].text)
    assert first.startswith('Aus Gründen der besseren Lesbarkeit'), first


def normalize_whitespaces(text: str) -> str:
    text = ' '.join(text.strip().split())
    return text


def test_footer_homework18(testdir, monkeypatch):
    extracted = tests.groupme_.footerheader.extractor.footer(
        power.HOME018_PDF,
        testdir,
        monkeypatch,
        pages='3:17',
    )
    content = utila.flatten([item.footer.notes for item in extracted])
    # TODO: Change after fixing footnote merger
    assert len(content) == 96, len(content)
    # assert len(content) == 94, len(content)


def test_footer_bachelor51(testdir, monkeypatch):
    extracted = tests.groupme_.footerheader.extractor.footer(
        power.BACHELOR051_PDF,
        testdir,
        monkeypatch,
    )
    pages = [item.footer.page.value for item in extracted]
    assert len(pages) >= 23


def test_footer_master110(testdir, monkeypatch):
    extracted = tests.groupme_.footerheader.extractor.footer(
        power.MASTER110_PDF,
        testdir,
        monkeypatch,
    )
    footers = [item.footer for item in extracted if item.footer]
    # changes in the future if data generator is extended
    assert len(footers) == 37


def test_footer_master99_page8(testdir, monkeypatch):
    extracted = tests.groupme_.footerheader.extractor.footer(
        power.MASTER099_PDF,
        testdir,
        monkeypatch,
        pages='8',
    )
    footer = extracted[0].footer.notes[0].text.strip()
    footer = utila.normalize_whitespaces(footer)
    assert footer.startswith('Näheres')
    assert footer.endswith('nachgelesen werden.')
