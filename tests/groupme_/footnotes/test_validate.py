# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import pytest
import serializeraw
import utila

import groupme
import tests.groupme_

EXPECTED = os.path.join(groupme.ROOT, 'tests/groupme_/footnotes/expected')
file_read = lambda x: utila.file_read(os.path.join(EXPECTED, x)).strip()  # pylint:disable=C0103


# yapf:disable
@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.BACHELOR128_PDF, '0:14', 'bachelor128', id='bachelor128'),
    pytest.param(power.HOME018_PDF, None, 'home018', id='home018'),
    pytest.param(power.DISS143_PDF, None, 'diss143', id='diss143all'),
    pytest.param(power.DISS143_PDF, '20:26', 'diss143page20', id='diss143page20'),
])
# yapf:enable
# @utilatest.nightly
def test_footnotes_validate(source, pages, expected, testdir, monkeypatch):
    pages = '' if pages is None else f'--pages={pages}'
    cmd = f'-i {power.link(source)}  --footer {pages}'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)
    # verify
    loaded = serializeraw.load_footnotes(testdir.tmpdir)
    footnotes = plain(loaded)
    expected = file_read(expected)
    assert footnotes == expected


def plain(footnotes) -> str:
    footnotes = utila.flatten_content(footnotes)
    footnotes = [utila.normalize_text(item.text.strip()) for item in footnotes]
    result = utila.NEWLINE.join(footnotes)
    return result
