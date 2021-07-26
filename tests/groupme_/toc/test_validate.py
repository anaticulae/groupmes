# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import power
import pytest
import serializeraw
import utila
import utilatest

import groupme
import groupme.path
import tests

EXPECTED = os.path.join(groupme.ROOT, 'tests/groupme_/toc/expected')
file_read = lambda x: utila.file_read(os.path.join(EXPECTED, x)).strip()  # pylint:disable=C0103


def merge_required(toc: iamraw.Toc) -> str:
    result = []

    def recursive(item, level):
        result = []
        result.append('    ' * level + item.title)
        assert item.raw_location >= 0, str(item)
        if item.children:
            for child in item.children:
                result.extend(recursive(child, level + 1))
        return result

    for item in toc:
        result.extend(recursive(item, level=0))
    titles = utila.NEWLINE.join(result)
    return titles


TEN = utila.make_tuple(10)


# yapf:disable, format the list by hand
@pytest.mark.parametrize('source, validate, pages', [
    pytest.param(power.BACHELOR076_PDF, 'bachelor076', TEN, id='bachelor76'),
    pytest.param(power.BACHELOR111_PDF, 'bachelor111', (1, 2, 3, 4), id='bachelor111',
                 marks=pytest.mark.xfail(reason='literaturverzeichnis sub notes')),
    pytest.param(power.BACHELOR241_PDF, 'bachelor241', (4, 5, 6, 7), id='bachelor241',
                 marks=pytest.mark.xfail(reason='literaturverzeichnis sub notes')),
    pytest.param(power.HOME050_PDF, 'homework050', (3, 4), id='homework50'),
    pytest.param(power.MASTER083_PDF, 'master083', TEN, id='master83'),
    pytest.param(power.MASTER089_PDF, 'master089', TEN, id='master89'),
    pytest.param(power.MASTER098_PDF, 'master098', TEN, id='master98'),
    pytest.param(power.MASTER099_PDF, 'master099', TEN, id='master99'),
    pytest.param(power.MASTER072_PDF, 'master072', None, id='master72'),
    pytest.param(power.BACHELOR090_PDF, 'bachelor090', TEN, id='bachelor90',
            marks=pytest.mark.xfail(reason='investigate later')),
    pytest.param(power.BACHELOR063_PDF, 'bachelor063', TEN, id='bachelor63'),
    pytest.param(power.MASTER078_PDF, 'master078', TEN, id='master78'),
    pytest.param(power.DISS180_PDF, 'diss180', (4, 5), id='diss180'),
])
# yapf:enable
@utilatest.nightly
def test_toc_validate(source, validate, pages, monkeypatch, testdir):
    """Verify parsing behavior and check that toc is located
    automatically in range of `TEN` pages."""
    source = power.link(source)
    pages = utila.from_tuple(pages, separator=',') if pages else ':'
    cmd = f'-i {source} --toc --pages={pages}'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)

    toc = serializeraw.load_toc(testdir.tmpdir)

    if callable(validate):
        validate(toc)
        return
    validate = file_read(validate)
    titles = merge_required(toc)
    assert titles == validate, validate
