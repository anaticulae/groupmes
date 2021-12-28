# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
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
import tests.groupme_

ARCHIVE = os.path.join(groupme.ROOT, 'tests/groupme_/footnotes/expected')


# yapf:disable
@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.BACHELOR128_PDF, '0:14', 'bachelor128', id='bachelor128'),
    pytest.param(power.HOME018_PDF, None, 'home018', id='home018'),
    pytest.param(power.DISS143_PDF, None, 'diss143', id='diss143all'),
    pytest.param(power.DISS143_PDF, '20:26', 'diss143page20', id='diss143page20'),
    pytest.param(power.BACHELOR037_PDF, None, 'bachelor037', id='bachelor037'),
])
# yapf:enable
@utilatest.longrun
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
                tests.groupme_.run,
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
        footnotes = [
            utila.normalize_text(item.text.strip()) for item in footnotes
        ]
        result = utila.NEWLINE.join(footnotes)
        return result
