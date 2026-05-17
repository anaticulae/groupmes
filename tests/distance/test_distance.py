# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import utilatest

import groupmes.feature.distance
import groupmes.path


def docu007(pages: tuple = None):
    utilatest.fixture_requires(power.DOCU007_PDF)
    # TODO: REMOVE DUPLICATION
    source = power.link(power.DOCU007_PDF)
    area = groupmes.path.area(source)
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)
    loaded = groupmes.feature.distance.load(
        area,
        text,
        textposition,
        pages=pages,
    )
    return loaded


@pytest.mark.xfail(reason='investigate later')
def test_distance_pyport_page0():
    loaded = docu007(pages=(0))
    distances = groupmes.feature.distance.determine_distances(loaded)
    first = distances[0].content[0]
    assert first.after >= 40, first.after
    assert first.before <= -16, first.before


def test_distance_pyport_page3():
    loaded = docu007(pages=(3))
    distances = groupmes.feature.distance.determine_distances(loaded)
    page = distances[0].content
    assert len(page) == 1, page
    first = page[0]
    assert first.before < 0, first
    assert first.after > 0, first


@pytest.mark.xfail(reason='improve table parser')
def test_distance_pyport_page5():
    loaded = docu007(pages=(5))
    distances = groupmes.feature.distance.determine_distances(loaded)
    page = distances[0].content
    assert len(page) == 4, page
    assert all((item.after is None or item.after >= 0.0 for item in page))
    assert all((item.before is None or item.before < 0.0 for item in page))


def test_distance_pyport():
    loaded = docu007()
    distances = groupmes.feature.distance.determine_distances(loaded)
    assert len(distances) == 3, distances


def test_distance_dump_load():
    data = docu007()
    distances = groupmes.feature.distance.determine_distances(data)

    dumped = groupmes.feature.distance.dump_distance(distances)
    loaded = groupmes.feature.distance.load_distance(dumped)
    assert loaded == distances
