# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw

import groupme.footer.strategy.pages


@pytest.mark.parametrize(
    'document,  expected_pagenumbers',
    [
        pytest.param(power.link(power.DOCU14_PDF), 14, id='docu14'),
        pytest.param(
            power.link(power.TECH024_PDF),
            # header page has no page number
            24 - 1,
            id='technical24pages',
        ),
    ])
def test_footer_pagenumber_strategy(
    document,
    expected_pagenumbers,
):
    horizontallines = serializeraw.load_horizontals(
        iamraw.path.horizontals(document),)
    sizeandborder = serializeraw.load_pageborders(
        iamraw.path.sizeandborder(document),)
    pagenumbers = serializeraw.load_pagenumbers(
        groupme.path.pagenumbers(document),)

    pagetextnavigators = serializeraw.create_pagetextnavigators_frompath(
        document,)

    strategy = groupme.footer.strategy.pages.PageNumberStrategy(
        horizontals=horizontallines,
        sizeandborders=sizeandborder,
        pagenumbers=pagenumbers,
        pagetextnavigators=pagetextnavigators,
    )

    result = strategy.result()

    assert result is not None, result
    assert len(result) == expected_pagenumbers, result
