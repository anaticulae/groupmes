# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utilatest

import groupme.footer.strategy.pages


@pytest.mark.parametrize(
    'source, expected',
    [
        pytest.param(power.link(power.DOCU014_PDF), 14, id='docu14'),
        pytest.param(power.link(power.MASTER091A_PDF), 86, id='master91a'),
        pytest.param(
            power.link(power.TECH024_PDF),
            # header page has no page number
            24 - 1,
            id='technical24pages',
        ),
    ])
@utilatest.longrun
def test_footer_pagenumber_strategy(source, expected):
    # prepare data
    horizontallines = serializeraw.load_horizontals(source)
    sizeandborder = serializeraw.load_pageborders(source)
    pagenumbers = serializeraw.load_pagenumbers(source)
    pagetextnavigators = serializeraw.create_pagetextnavigators_frompath(source)
    strategy = groupme.footer.strategy.pages.PageNumberStrategy(
        horizontals=horizontallines,
        sizeandborders=sizeandborder,
        pagenumbers=pagenumbers,
        pagetextnavigators=pagetextnavigators,
    )
    # run strategy
    result = strategy.result()
    # verify
    assert result is not None, result
    assert len(result) == expected, result
