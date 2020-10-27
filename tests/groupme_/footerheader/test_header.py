# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw
import utilatest

import groupme.feature.footer
import groupme.path
import tests.groupme_


@pytest.mark.parametrize('root, expected', [
    pytest.param(
        power.link(power.TECH024_PDF),
        list(range(1, 24)),
        id='technical24',
    ),
    pytest.param(
        power.link(power.MASTER072_PDF),
        [],
        id='master72',
    ),
])
@utilatest.longrun
def test_footer_extract_footerheader_technical(root, expected):
    pages = None
    pagetextnavigators = serializeraw.create_pagetextnavigators_frompath(
        root,
        pages=pages,
    )
    horizontals = serializeraw.load_horizontals(root, pages=pages)
    sizeandborders = serializeraw.load_pageborders(root, pages=pages)
    pagenumbers = serializeraw.load_pagenumbers(
        groupme.path.pagenumbers(root),
        pages=pages,
    )
    result = groupme.feature.footer.extract_footerheader(
        horizontals=horizontals,
        sizeandborders=sizeandborders,
        pagenumbers=pagenumbers,
        pagetextnavigators=pagetextnavigators,
    )

    header = [item.page for item in result if item.header is not None]
    assert header == expected


def extract_header(source, testdir, monkeypatch, pages=':'):
    cmd = f'-i {power.link(source)}  --footer --pages={pages}'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)
    headerpath = iamraw.path.headerfooters(testdir.tmpdir)

    loaded = serializeraw.load_headerfooter(headerpath)
    header = [item.header for item in loaded if item.header]
    return header


def test_header_bachelor90(testdir, monkeypatch):
    header = extract_header(power.BACHELOR090_PDF, testdir, monkeypatch, '11:24') # yapf:disable
    assert len(header) == 11


@utilatest.longrun
def test_header_bachelor37_starting_index(testdir, monkeypatch):
    """Ensure that parts of pages `4:20` for example are indexed correctly."""
    header = extract_header(power.BACHELOR037_PDF, testdir, monkeypatch, '4:20')
    assert header[0].page.value == 4


@utilatest.longrun
def test_header_bachelor37_all(testdir, monkeypatch):
    header = extract_header(power.BACHELOR037_PDF, testdir, monkeypatch)

    noheader = [0, 5, 33]
    expected = [item for item in range(0, 37) if item not in noheader]
    current = [item.page.value for item in header]
    assert current == expected


@utilatest.longrun
def test_header_diss264_page0_40(testdir, monkeypatch):
    header = extract_header(
        power.DISS264_PDF,
        testdir,
        monkeypatch,
        pages='0:40',
    )
    assert len(header) == 37


@utilatest.longrun
def test_header_diss264_all(testdir, monkeypatch):
    """Ensure to parse header of alternating pages correctly."""
    loaded = extract_header(power.DISS264_PDF, testdir, monkeypatch, '0:150')
    assert len(loaded) == 47  # may change in the future


@utilatest.longrun
def test_header_under_line_master75(testdir, monkeypatch):
    """Ensure to parse header of alternating pages correctly."""
    loaded = extract_header(power.MASTER075_PDF, testdir, monkeypatch, '0:50')
    assert len(loaded) == 48, len(loaded)

    # TODO: MAY ENABLE LATER
    # first = loaded[0].header.undefined
    # use common extractor
    # assert len(first) == 2, str(first)


@utilatest.longrun
def test_header_master110(testdir, monkeypatch):
    loaded = extract_header(power.MASTER110_PDF, testdir, monkeypatch, '0:50')
    assert len(loaded) == 25  # may change in the future


@utilatest.longrun
def test_header_master155(testdir, monkeypatch):
    loaded = extract_header(power.MASTER155_PDF, testdir, monkeypatch)
    assert len(loaded) == 153  # do not change
