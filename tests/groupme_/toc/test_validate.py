# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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


@pytest.mark.parametrize('source, pages', [
    utilatest.step(power.BACHELOR063_PDF, TEN),
    utilatest.step(power.BACHELOR076_PDF, TEN),
    utilatest.step(power.BACHELOR090_PDF, TEN, reason='investigate laster'),
    utilatest.step(power.BACHELOR111_PDF, (1, 2, 3, 4), reason='sub notes'),
    utilatest.step(power.BACHELOR241_PDF, (4, 5, 6, 7), reason='sub notes'),
    utilatest.step(power.DISS157_PDF, (6, 7, 8)),
    utilatest.step(power.DISS180_PDF, (4, 5)),
    utilatest.step(power.HOME050_PDF, (3, 4)),
    utilatest.step(power.MASTER072_PDF, None),
    utilatest.step(power.MASTER078_PDF, TEN),
    utilatest.step(power.MASTER083_PDF, TEN),
    utilatest.step(power.MASTER089_PDF, TEN),
    utilatest.step(power.MASTER098_PDF, TEN),
    utilatest.step(power.MASTER099_PDF, TEN),
    utilatest.step(power.DISS406_PDF, (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)),
    utilatest.step(power.MASTER099B_PDF, (2,)),
    utilatest.step(power.MASTER049_PDF, (4,)),
    utilatest.step(power.MASTER155_PDF, (1, 2)),
])
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
