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
import utilatest

import groupme


@pytest.mark.parametrize('resource, expected', [
    pytest.param(power.link(power.BACHELOR111_PDF), 110, id='bachelor111'),
    pytest.param(power.link(power.MASTER072_PDF), 69, id='master72pages'),
    pytest.param(power.link(power.TECH024_PDF), 23, id='technical24pages'),
    pytest.param(power.link(power.MASTER091A_PDF), 88, id='master91a'),
])
@utilatest.longrun
def test_validate_pagenumbers(resource, expected):
    # TODO: bottom only, add header page extraction
    text = iamraw.path.text(resource)
    text_positions = iamraw.path.textposition(resource)

    result = groupme.feature.pagenumbers.work(text, text_positions)
    result = serializeraw.load_pagenumbers(result)

    if isinstance(result, tuple):
        # left right, or multiple pages positions
        result = result[0] + result[1]
    assert isinstance(result, list), f' page detection type {type(result)}'
    assert len(result) == expected
