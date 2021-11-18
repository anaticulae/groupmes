# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
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

import groupme


def bachelor111(result):
    assert len(result) == 110
    expected = 'i ii iii iv'.split() + utila.ranged_list(start=1, end=107)
    current = [item.detected for item in result]
    assert current == expected


# master110: 86 and xii is currently not detected
# VALIDATED: master110: 110-15
@pytest.mark.parametrize('source, expected', [
    pytest.param(power.BACHELOR111_PDF, bachelor111, id='bachelor111'),
    pytest.param(power.MASTER072_PDF, 69, id='master72pages'),
    pytest.param(power.TECH024_PDF, 23, id='technical24pages'),
    pytest.param(power.MASTER091A_PDF, 88, id='master91a'),
    pytest.param(power.MASTER110_PDF, 91, id='master110'),
    pytest.param(power.MASTER127_PDF, 127 - 1, id='master127'),
])
@utilatest.longrun
def test_validate_pagenumbers(source, expected):
    extracted = power.link(source)
    # TODO: bottom only, add header page extraction
    text = iamraw.path.text(extracted)
    text_positions = iamraw.path.textposition(extracted)
    # run extractor
    result = groupme.feature.pagenumbers.work(text, text_positions)
    result = serializeraw.load_pagenumbers(result)
    if callable(expected):
        expected(result)
        return
    if isinstance(result, tuple):
        # left right, or multiple pages positions
        result = result[0] + result[1]
    assert isinstance(result, list), f' page detection type {type(result)}'
    assert len(result) == expected
