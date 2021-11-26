# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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

ARCHIVE = os.path.join(groupme.ROOT, 'tests/groupme_/toc/expected')
TEN = utila.make_tuple(10)


# yapf:disable, format the list by hand
@pytest.mark.parametrize('source, pages', [
    pytest.param(power.BACHELOR076_PDF, TEN, id='bachelor76'),
    pytest.param(power.BACHELOR111_PDF, (1, 2, 3, 4), id='bachelor111',
                marks=pytest.mark.xfail(reason='literaturverzeichnis sub notes')),
    pytest.param(power.BACHELOR241_PDF, (4, 5, 6, 7), id='bachelor241',
                marks=pytest.mark.xfail(reason='literaturverzeichnis sub notes')),
    pytest.param(power.HOME050_PDF, (3, 4), id='homework50'),
    pytest.param(power.MASTER083_PDF, TEN, id='master83'),
    pytest.param(power.MASTER089_PDF, TEN, id='master89'),
    pytest.param(power.MASTER098_PDF, TEN, id='master98'),
    pytest.param(power.MASTER099_PDF, TEN, id='master99'),
    pytest.param(power.MASTER072_PDF, None, id='master72'),
    pytest.param(power.BACHELOR090_PDF, TEN, id='bachelor90',
                marks=pytest.mark.xfail(reason='investigate later')),
    pytest.param(power.BACHELOR063_PDF, TEN, id='bachelor63'),
    pytest.param(power.MASTER078_PDF, TEN, id='master78'),
    pytest.param(power.DISS180_PDF, (4, 5), id='diss180'),
    pytest.param(power.DISS157_PDF, (6,7,8), id='diss157'),
])
# yapf:enable
@utilatest.nightly
def test_toc_validate(source, pages, monkeypatch, testdir):
    """Verify parsing behavior and check that toc is located
    automatically in range of `TEN` pages."""
    pages = utila.from_tuple(pages, ',') if pages else ':'
    Evaluate(source, pages, testdir.tmpdir, monkeypatch).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                tests.groupme_.run,
                monkeypatch=monkeypatch,
            ),
            step='toc',
            source=source,
            pages=pages,
            workdir=workdir,
            archive=ARCHIVE,
            loader=serializeraw.load_toc,
        )

    def raw(self, value) -> str:
        result = []
        for item in value:
            result.extend(self.recursive(item, level=0))
        titles = utila.NEWLINE.join(result)
        return titles

    def recursive(self, item, level):
        result = ['    ' * level + item.title]
        assert item.raw_location >= 0, str(item)
        if not item.children:
            return result
        for child in item.children:
            result.extend(self.recursive(child, level + 1))
        return result
