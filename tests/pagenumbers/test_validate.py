# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import iamraw
import power
import pytest
import serializeraw
import utila
import utilatest

import groupme
import groupme.feature.pagenumbers
import tests

ARCHIVE = utila.join(groupme.ROOT, 'tests/pagenumbers/expected')


def bachelor085(result):  # pylint:disable=W0613
    """Enable after fixing rawmaker text extractor."""
    return
    # current = [item.detected for item in result]
    # expected = []
    # assert current == expected
    # assert len(current) == 78


def bachelor111(result):
    assert len(result) == 110
    expected = 'i ii iii iv'.split() + utila.ranged_list(start=1, end=107)
    current = [item.detected for item in result]
    assert current == expected


def master110(result):
    # VALIDATED: master110: 110-15?
    assert len(result) == 91
    current = [item.detected for item in result]
    # master110: 86 and xii is currently not detected
    expected = [
        'iii', 'v', 'vii', 'ix', 'xi', 'xiii', 'xv', 'xvii', 1, 2, 3, 5, 6, 7,
        8, 9, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
        28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46,
        47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 65,
        66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 81, 82, 83, 85,
        87, 88, 89, 90, 91
    ]
    assert current == expected


def master049(result):
    assert len(result) == 45
    current = [item.detected for item in result]
    expected = [
        'ii', 'iii', 'iv', 'v', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
        15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
        33, 34, 35, 36, 37, 38, 39, 40, 41
    ]
    assert current == expected


def diss148(result):
    """This document contains a lot of paper as a part accumulative diss."""
    current = [item.detected for item in result]
    expected = [
        'i', 'ii', 'iii', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
        17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
        35, 43, 2, 3, 4, 5, 49, 15839, 15840, 15841, 15842, 15843, 15844, 15845,
        15846, 62, 78, 79, 80, 81, 82, 83, 84, 85, 79, 106, 107, 108, 109, 110,
        111, 112, 113, 114, 115, 117, 118, 119, 120, 121, 122, 123, 124, 125,
        126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137
    ]
    assert current == expected


def diss170b(result):
    current = [item.detected for item in result]
    # TODO: MISSING PAGE 144 and PAGE 145
    expected = [
        'I', 'II', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
        18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
        36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
        54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,
        72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89,
        90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105,
        106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119,
        120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133,
        134, 135, 136, 137, 138, 139, 140, 141, 142, 145, 146, 147, 148, 149,
        150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163,
        164, 165, 166, 167, 168
    ]
    assert current == expected


def diss480(result):
    current = [item.detected for item in result]
    assert utila.isascending(current)


def diss218(result):
    current = [item.detected for item in result]
    assert utila.isascending(current)


def diss287(result):
    current = [item.detected for item in result]
    expected = [
        'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI',
        'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 1, 2, 3, 4, 5, 6, 7, 8, 9,
        10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
        28, 29, 30, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
        48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65,
        66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80
    ]
    assert current == expected
    assert len(current) == 78


HUNDRED = utila.ranged_list(100)


@pytest.mark.parametrize('source,pages,expected', [
    pytest.param(power.BACHELOR085_PDF, None, bachelor085, id='bachelor085'),
    pytest.param(power.BACHELOR111_PDF, None, bachelor111, id='bachelor111'),
    pytest.param(power.DISS148_PDF, None, diss148, id='diss148'),
    pytest.param(power.DISS170B_PDF, None, diss170b, id='diss170b'),
    pytest.param(power.DISS218_PDF, HUNDRED, diss218, id='diss218'),
    pytest.param(power.DISS287_PDF, None, diss287, id='diss287'),
    pytest.param(power.DISS406_PDF, None, 119, id='diss406'),
    pytest.param(power.DISS480_PDF, None, diss480, id='diss480'),
    pytest.param(power.MASTER049_PDF, None, master049, id='master049'),
    pytest.param(power.MASTER072_PDF, None, 69, id='master72pages'),
    pytest.param(power.MASTER091A_PDF, None, 88, id='master91a'),
    pytest.param(power.MASTER110_PDF, None, master110, id='master110'),
    pytest.param(power.MASTER127_PDF, None, 127 - 1, id='master127'),
])
@utilatest.nightly
def test_validate_pagenumbers(source, pages, expected):
    extracted = power.link(source)
    # TODO: bottom only, add header page extraction
    # run extractor
    result = groupme.feature.pagenumbers.work(
        iamraw.path.text(extracted),
        iamraw.path.textposition(extracted),
        pages=pages,
    )
    result = serializeraw.load_pagenumbers(result)
    if callable(expected):
        expected(result)
        return
    if isinstance(result, tuple):
        # left right, or multiple pages positions
        result = result[0] + result[1]
    assert isinstance(result, list), f' page detection type {type(result)}'
    assert len(result) == expected


@pytest.mark.parametrize('source', [
    pytest.param(power.TECH024_PDF, id='tech024'),
])
def test_pagenumber_validate(source, monkeypatch, testdir):
    Evaluate(
        source=source,
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                tests.run,
                monkeypatch=monkeypatch,
            ),
            step='pagenumbers',
            source=source,
            pages=':',
            workdir=workdir,
            archive=ARCHIVE,
            loader=serializeraw.load_pagenumbers,
        )

    def raw(self, value) -> str:
        if not value:
            return ''
        if isinstance(value, tuple):
            # left right, or multiple pages positions
            value = value[0] + value[1]
        assert isinstance(value, list), f' page detection type {type(value)}'
        maxpage = value[-1].pdfpage
        collected = {pdfpage: '' for pdfpage in range(maxpage)}
        for item in value:
            collected[item.pdfpage] = str(item.detected)
        result: str = utila.NEWLINE.join(collected.values())
        return result
