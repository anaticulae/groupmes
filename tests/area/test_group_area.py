# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import hoverpower
import pytest
import utilo
import utilotest

import groupmes.feature.area


def docu007(pages: tuple = None):
    utilotest.fixture_requires(hoverpower.DOCU007_PDF)
    source = hoverpower.link(hoverpower.DOCU007_PDF)
    text = iamraw.path.text(source)
    textpositions = iamraw.path.textposition(source)
    tables = iamraw.path.tablero_result(source)
    boxes = iamraw.path.boxed(source)
    loaded = groupmes.feature.area.load(
        boxes=boxes,
        tables=tables,
        text=text,
        textpositions=textpositions,
        pages=pages,
    )
    return loaded


def test_area_docu007_table():
    loaded = docu007(pages=3)
    grouped = groupmes.feature.area.group_areas(loaded)
    assert grouped
    assert len(grouped[0].outside['tables']) == 6


@pytest.mark.xfail(reason='???')
def test_area_docu007_boxes():
    loaded = docu007(pages=5)
    grouped = groupmes.feature.area.group_areas(loaded)
    assert grouped
    assert len(grouped) == 1
    # elements inside boxes
    assert len(grouped[0].outside['boxes']) == 17


def test_area_dump_load():
    data = docu007()
    grouped = groupmes.feature.area.group_areas(data)

    assert grouped
    dumped = groupmes.feature.area.dump_area(grouped)
    loaded = groupmes.feature.area.load_area(dumped)
    assert grouped == loaded


def test_area_rect_merge():
    before = [
        (10, 10, 100, 100),
        (10, 10, 30, 30),
        (90, 10, 150, 100),
        (30, 30, 60, 70),
    ]
    expected = [
        (10, 10, 100, 100),
        (90, 10, 150, 100),
    ]

    merged = utilo.rect_merge(before)
    assert merged == expected

    before = [
        (10, 10, 100, 100),
        (25, 25, 50, 50),
        (50, 50, 75, 75),
        (75, 75, 100, 100),
    ]
    expected = [
        (10, 10, 100, 100),
    ]

    merged = utilo.rect_merge(before)
    assert merged == expected
