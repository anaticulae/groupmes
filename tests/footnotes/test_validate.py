# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import os

import power
import pytest
import serializeraw
import utila
import utilatest

import groupme
import tests

ARCHIVE = os.path.join(groupme.ROOT, 'tests/footnotes/expected')
utila.exists_assert(ARCHIVE)


# yapf:disable
@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.BACHELOR037_PDF, None, 'bachelor037', id='bachelor037'),
    pytest.param(power.BACHELOR128_PDF, '0:14', 'bachelor128', id='bachelor128'),
    pytest.param(power.DISS143_PDF, '20:26', 'diss143page20', id='diss143page20'),
    pytest.param(power.DISS143_PDF, None, 'diss143', id='diss143all'),
    pytest.param(power.DISS172_PDF, None, 'diss172', id='diss172'),
    pytest.param(power.DISS178_PDF, '0:30', 'diss178', id='diss178'),
    pytest.param(power.DISS273_PDF, '30:60', 'diss273', id='diss273'),
    pytest.param(power.DISS406_PDF, '0:50', 'diss406', id='diss406'),
    pytest.param(power.DISS480_PDF, '4,5', 'diss480p4p5', id='diss480p4p5'),
    pytest.param(power.HOME018_PDF, None, 'home018', id='home018'),
    pytest.param(power.MASTER127_PDF, ':', 'master127', id='master127'),
])
# yapf:enable
@utilatest.nightly
def test_footnotes_validate(source, pages, expected, testdir, monkeypatch):
    Evaluate(
        source=source,
        pages=pages,
        expected=expected,
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                tests.run,
                monkeypatch=monkeypatch,
            ),
            step='footer',
            pages=pages,
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.load_footnotes,
            convert_source=False,
            index=expected,
        )

    def load_footnotes(self, _):  # pylint:disable=W0613
        loaded = serializeraw.load_footnotes(self.workdir)
        return loaded

    def raw(self, value) -> str:
        footnotes = utila.flatten_content(value)
        footnotes = [rawline(item) for item in footnotes]
        result = utila.NEWLINE.join(footnotes)
        return result


def rawline(footnote) -> str:
    if footnote.raw_number is not None:
        result = str(footnote.number).zfill(4) + ' '
    else:
        result = '     '
    result += utila.normalize_text(footnote.text.strip())
    return result
