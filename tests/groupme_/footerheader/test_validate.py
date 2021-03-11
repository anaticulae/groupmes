# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import pytest
import serializeraw
import utila
import utilatest

import tests.groupme_


def homework18(footnotes):
    assert len(footnotes) == 96  # TODO: 94!


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.HOME018_PDF, None, homework18, id='homework18'),
    pytest.param(power.BACHELOR063_PDF, None, 0, id='bachelor63'),
    pytest.param(power.MASTER116_PDF, None, 0, id='master116'),
])
@utilatest.longrun
def test_footer_validate(source, pages, expected, testdir, monkeypatch):
    pages = '' if pages is None else f'--pages={pages}'
    cmd = f'-i {power.link(source)}  --footer {pages}'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)

    footnotes = serializeraw.load_footnotes(testdir.tmpdir)
    footnotes = utila.flatten_content(footnotes)

    expected = 0 if expected is None else expected
    if callable(expected):
        expected(footnotes)
    else:
        assert len(footnotes) == expected, len(footnotes)
