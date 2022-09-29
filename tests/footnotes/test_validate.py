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

ARCHIVE = utila.join(groupme.ROOT, 'tests/footnotes/expected', exist=True)

step = lambda x: pytest.param(x, ':', utila.file_name(x), id=utila.file_name(x))

RESOURCES = (
    power.BACHELOR028_PDF,
    power.BACHELOR032A_PDF,
    power.BACHELOR032_PDF,
    power.BACHELOR037_PDF,
    power.BACHELOR039_PDF,
    power.BACHELOR041A_PDF,
    power.BACHELOR056_PDF,
    power.BACHELOR063_PDF,
    power.BACHELOR077_PDF,
    power.BACHELOR078_PDF,
    power.BACHELOR086_PDF,
    power.BACHELOR101_PDF,
    power.BACHELOR105_PDF,
    power.BACHELOR111_PDF,
    power.DISS143_PDF,
    power.DISS172_PDF,
    power.DOCU014_PDF,
    power.DOCU027_PDF,
    power.HC_BACH106,
    power.HC_DISS128,
    power.HC_DISS148,
    power.HC_DISS166,
    power.HC_DISS171,
    power.HC_DISS193,
    power.HOME018_PDF,
    power.MASTER063_PDF,
    power.MASTER072_PDF,
    power.MASTER075_PDF,
    power.MASTER089_PDF,
    power.MASTER091A_PDF,
    power.MASTER091B_PDF,
    power.MASTER099C_PDF,
    power.MASTER110_PDF,
    power.MASTER112_PDF,
    power.MASTER116_PDF,
    power.MASTER127_PDF,
    power.MASTER155_PDF,
    power.MASTER193_PDF,
    power.PAPER14B_PDF,
    power.PAPER18_PDF,
    power.TECH024_PDF,
)


@pytest.mark.parametrize('source', utilatest.test_resources(RESOURCES))
@utilatest.nightly
def test_validate_footnotes_all(source, td, mp):
    Evaluate(
        source=source,
        pages=':',
        expected=None,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.BACHELOR128_PDF, '0:14', 'bachelor128', id='bachelo128'),
    pytest.param(power.DISS143_PDF, '20:26', 'diss143page20', id='diss143p20'),
    pytest.param(power.DISS178_PDF, '0:30', 'diss178', id='diss178'),
    pytest.param(power.DISS273_PDF, '30:60', 'diss273', id='diss273'),
    pytest.param(power.DISS406_PDF, '0:50', 'diss406', id='diss406'),
    pytest.param(power.DISS480_PDF, '4,5', 'diss480p4p5', id='diss480p4p5'),
])
@utilatest.nightly
def test_validate_footnotes_selected(source, pages, expected, td, mp):
    Evaluate(
        source=source,
        pages=pages,
        expected=expected,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, mp):
        super().__init__(
            program=functools.partial(
                tests.run,
                mp=mp,
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
    result = '     '
    if footnote.raw_number is not None:
        result = str(footnote.number).zfill(4) + ' '
    result += utila.normalize_text(footnote.text.strip())
    return result
