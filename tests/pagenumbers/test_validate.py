# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import pytest
import serializeraw
import utila
import utilatest

import groupme
import tests

ARCHIVE = utila.join(groupme.ROOT, 'tests/pagenumbers/expected', exist=True)

RESOURCES = [
    power.BACHELOR085_PDF,
    power.BACHELOR111_PDF,
    power.DISS148_PDF,
    power.DISS170B_PDF,
    power.DISS218_PDF,
    power.DISS287_PDF,
    power.DISS406_PDF,
    power.DISS480_PDF,
    power.HC_DISS128,
    power.HC_DISS148,
    power.HC_DISS166,
    power.HC_DISS171,
    power.HC_DISS193,
    power.MASTER049_PDF,
    power.MASTER072_PDF,
    power.MASTER091A_PDF,
    power.MASTER110_PDF,
    power.MASTER127_PDF,
    power.PAPER14B_PDF,
    power.PAPER18_PDF,
    power.TECH024_PDF,
]
PAGENUMBERS = [pytest.param(pdf, id=utila.file_name(pdf)) for pdf in RESOURCES]


@utilatest.longrun
@pytest.mark.parametrize('source', PAGENUMBERS)
def test_validate_pagenumbers(source, monkeypatch, testdir):
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
