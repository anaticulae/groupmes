# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw

import groupme.footer.strategy.pages


@pytest.mark.parametrize(
    'document, pages, expected_pagenumbers',
    [
        pytest.param(power.link(power.DOCU14_PDF), 14, 14, id='docu14'),
        pytest.param(
            power.link(power.TECH024_PDF),
            24,
            # header page has no page number
            24 - 1,
            id='technical24pages',
        ),
    ])
def test_footer_pagenumber_strategy(
    document,
    pages,
    expected_pagenumbers,
):
    pages = tuple(range(pages))
    horizontallines = serializeraw.load_horizontals(
        iamraw.path.horizontals(document),
        pages,
    )
    sizeandborder = serializeraw.load_pageborders(
        iamraw.path.sizeandborder(document),
        pages,
    )
    pagenumbers = serializeraw.load_pagenumbers(
        groupme.path.pagenumbers(document),
        pages,
    )

    pagetextnavigators = serializeraw.create_pagetextnavigators_frompath(
        document,
        pages=pages,
    )

    strategy = groupme.footer.strategy.pages.PageNumberStrategy(
        horizontals=horizontallines,
        sizeandborders=sizeandborder,
        pagenumbers=pagenumbers,
        pagetextnavigators=pagetextnavigators,
    )

    result = strategy.result()

    assert result is not None, result
    assert len(result) == expected_pagenumbers, result
