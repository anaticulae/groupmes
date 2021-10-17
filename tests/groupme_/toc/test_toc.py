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
import utila

import groupme.feature.toc
import groupme.pageselector
import groupme.toc.group


def test_toc_groupby_level():
    navigators = serializeraw.create_pagetextcontentnavigators_frompath(
        power.link(power.DOCU007_PDF),
        prefix='oneline',
    )
    selected = groupme.pageselector.select_contentpages(navigators)
    # select toc pages only
    navigators = [item for item in navigators if item.page in selected]
    loaded = groupme.toc.strategy.load(navigators)
    tableofcontent = groupme.toc.extractor.extract(loaded)

    tableofcontent = utila.flatten(tableofcontent.content)

    result = groupme.toc.group.groupby_level(tableofcontent)
    assert result
    dumped = serializeraw.dump_toc(result)
    assert dumped
    # TODO: Check level content


@pytest.mark.parametrize('resources, pages, expected', [
    pytest.param(
        power.link(power.DOCU027_PDF),
        (2,),
        13,
        id='restructured',
    ),
    pytest.param(
        power.link(power.DOCU007_PDF),
        (0,),
        12,
        marks=pytest.mark.xfail,
        id='simple',
    ),
    pytest.param(
        power.link(power.DOCU035_PDF),
        (5,),
        0,
        id='notoc',
    ),
])
def test_extract_toc_from_path(resources, pages, expected):
    navigators = serializeraw.create_pagetextcontentnavigators_frompath(
        path=resources,
        prefix='oneline',
        pages=pages,
    )
    loaded = groupme.toc.strategy.load(navigators)
    extracted = groupme.toc.extractor.extract(
        loaded,
        min_detection_count=groupme.feature.toc.TOC_COUNT_MIN,
    )
    flat = utila.flatten(extracted)
    assert len(flat) == expected, str(flat)
