# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
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

ARCHIVE = utila.join(
    groupme.ROOT,
    'tests/footerheader/expected',
    assert_exists=True,
)

step = lambda x: pytest.param(x, ':', utila.file_name(x), id=utila.file_name(x))


@pytest.mark.parametrize('source, pages, expected', [
    step(power.BOOK173_PDF),
])
@utilatest.longrun
def test_header_validate(source, pages, expected, testdir, monkeypatch):
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
        loaded = serializeraw.load_headerfooter(self.workdir)
        return loaded

    def raw(self, value) -> str:
        headers = [rawline(item.page, item.header) for item in value]
        # remove empty items
        headers = [item for item in headers if item]
        result = utila.NEWLINE.join(headers)
        return result


def rawline(pdfpage, header) -> str:
    if not header:
        return None
    if not any((header.title, header.undefined)):
        return None
    result = str(pdfpage).zfill(4) + ' '
    if header.title:
        result += header.title.raw
    undefined = ' '.join(item.text for item in header.undefined)
    if undefined:
        result += undefined
    return result
