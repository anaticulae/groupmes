# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw
import utila
import utilatest

import groupme.feature.footer
import groupme.footer.strategy.fixed
import groupme.footer.strategy.moving.run
import groupme.footer.strategy.pages
import groupme.path
import tests
import tests.footerheader.extractor


@utilatest.requires(power.DOCU027_PDF)
def test_footer_work(td):
    docu27 = power.link(power.DOCU027_PDF)
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
    utila.file_create(td.tmpdir.join('result.yaml'), dumped)


# TODO: CHECK 25
@pytest.mark.parametrize('strategy, expected_results', [
    (groupme.footer.strategy.moving.run.MovingFooterStrategy, 0),
    (groupme.footer.strategy.fixed.FixedFooterStrategy, 25),
    (groupme.footer.strategy.pages.PageNumberStrategy, 0),
])
@utilatest.requires(power.DOCU027_PDF)
def test_footer_footerheader_detectionstategy(
    strategy,
    expected_results,
):
    """Check that different strategies work proper with given resources

    TODO: SEE DUPLICATION test_footer_judgement_strategy_quality?"""
    source = power.link(power.DOCU027_PDF)
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


@utilatest.longrun
@utilatest.requires(power.MASTER072_PDF)
def test_footer_master72_extract(td, mp):
    outdir = td.tmpdir
    cmd = f'-i {power.link(power.MASTER072_PDF)}  -o {outdir} --footer --pages=3'
    tests.run(cmd, mp=mp)

    headfoot = serializeraw.load_headerfooter(iamraw.path.headerfooters(outdir))
    footnotes = headfoot[0].footer.notes
    assert len(footnotes) == 6, str(footnotes)

    first = utila.normalize_whitespaces(footnotes[0].text)
    assert first.startswith('Aus Gründen der besseren Lesbarkeit'), first


def test_footer_homework18(td, mp):
    extracted = tests.footerheader.extractor.footer(
        power.HOME018_PDF,
        td,
        mp,
        pages='3:17',
    )
    content = utila.flatten([item.footer.notes for item in extracted])
    assert len(content) == 94, len(content)


@utilatest.longrun
def test_footer_bachelor51(td, mp):
    """There are no footnotes. We have to verify pages-pattern.
    `current/maxpage`"""
    extracted = tests.footerheader.extractor.footer(
        power.BACHELOR051_PDF,
        td,
        mp,
        pages='0:25',
    )
    pages = [item.footer.page.value for item in extracted]
    assert len(pages) >= 23


@utilatest.longrun
def test_footer_master110(td, mp):
    extracted = tests.footerheader.extractor.footer(
        power.MASTER110_PDF,
        td,
        mp,
        pages='0:50',
    )
    footers = [item.footer for item in extracted if item.footer]
    # changes in the future if data generator is extended
    assert len(footers) == 37


def test_footer_master99_page8(td, mp):
    extracted = tests.footerheader.extractor.footer(
        power.MASTER099_PDF,
        td,
        mp,
        pages='8',
    )
    footer = extracted[0].footer.notes[0].text.strip()
    footer = utila.normalize_whitespaces(footer)
    assert footer.startswith('Näheres')
    assert footer.endswith('nachgelesen werden.')


@utilatest.nightly
def test_footer_master155_page107(td, mp):
    extracted = tests.footerheader.extractor.footer(
        power.MASTER155_PDF,
        td,
        mp,
        pages='0:110',
    )
    footer = utila.select_page(extracted, 107).footer
    assert isinstance(footer, iamraw.PagesFooterInformation), type(footer)


@utilatest.nightly
def test_footer_master127(td, mp):
    extracted = tests.footerheader.extractor.footer(
        power.MASTER127_PDF,
        td,
        mp,
        pages=':',
    )
    headers = [item.header for item in extracted if item.header is not None]
    assert len(headers) == 126  # VALIDATED
    footers = [
        item.footer
        for item in extracted
        if isinstance(item.footer, iamraw.MovingFooterInformation)
    ]
    assert len(footers) == 73  # VALIDATED
    footnotes = utila.flatten([item.notes for item in footers])
    assert len(footnotes) == 135  # VALIDATED


@utilatest.longrun
def test_footer_master075(td, mp):
    extracted = tests.footerheader.extractor.footer(
        power.MASTER075_PDF,
        td,
        mp,
        pages=':',
    )
    footers = [
        item.footer
        for item in extracted
        if isinstance(item.footer, iamraw.MovingFooterInformation)
    ]
    assert not footers
