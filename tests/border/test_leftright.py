# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import serializeraw
import utilotest

import groupmes.border.leftright
import tests


def load_example(path: str):
    utilotest.fixture_requires(path)
    # TODO: USE ONELINE?
    textpositions = serializeraw.load_textpositions(path)
    pagesizes = serializeraw.load_pageborders(path)
    return textpositions, pagesizes


def load_leftright(path: str):
    utilotest.fixture_requires(path)
    textpositions, pagesizes = load_example(path)
    left, right = groupmes.border.leftright.determine_pageborder(
        textpositions,
        pagesizes,
    )
    return left, right


def test_leftright_run():
    """Detect book-like document with different border for left and
    right page."""
    left, right = load_leftright(hoverpower.link(hoverpower.BOOK007_PDF))
    result = groupmes.border.leftright.simple(left, right)
    assert result.valid, result
    assert isinstance(result.left, tuple), result
    assert isinstance(result.right, tuple), result


@utilotest.requires(hoverpower.MASTER072_PDF)
def test_leftright_run_noleftright():
    """Ensure that document with single page layout has no different
    border for left and right but only a single border."""
    textpositions, pagesizes = load_example(
        hoverpower.link(hoverpower.MASTER072_PDF))
    result = groupmes.border.leftright.run(textpositions, pagesizes)
    assert not result.valid, result
    # ensure that left border is more left then right
    assert result.left < result.right, result


def test_leftright_one_error():
    """Introduce error to challenge algorithm."""
    left, right = load_leftright(hoverpower.link(hoverpower.BOOK007_PDF))

    left.append(left.pop(3))
    right.append(right.pop(3))

    result = groupmes.border.leftright.raising(left, right)
    assert result, result
    assert result.valid, result
    assert isinstance(result.left, tuple), result
    assert isinstance(result.right, tuple), result


def test_leftright_raising_bachelor241():
    left, right = load_leftright(hoverpower.link(hoverpower.BACHELOR241_PDF))
    result = groupmes.border.leftright.raising(left, right)
    assert result, result
    assert result.valid, result
    assert isinstance(result.left, tuple), result
    assert isinstance(result.right, tuple), result


def test_leftright_strategy_witherror():
    """Run left right strategy with example which contains an error."""
    textpositions, pagesizes = load_example(
        hoverpower.link(hoverpower.BOOK007_PDF))

    textpositions, pagesizes = introduce_error(textpositions, pagesizes)

    result = groupmes.border.leftright.run(textpositions, pagesizes)
    assert result, result
    assert result.valid, result
    assert isinstance(result.left, tuple), result
    assert isinstance(result.right, tuple), result


@utilotest.requires(hoverpower.BACHELOR241_PDF)
def test_leftright_bachelor241(td, mp):
    """Regression test to ensure that bachelor241 border is detected
    correctly."""
    source = hoverpower.link(hoverpower.BACHELOR241_PDF)
    tests.run(f'-i {source} --border', mp=mp)

    leftright = serializeraw.load_leftright_border(td.tmpdir)
    assert leftright[0] != leftright[1]


def introduce_error(left, right):
    left, right = left[:], right[:]
    # introduce an error
    left.append(left.pop(3))
    right.append(right.pop(3))

    lresult, rresult = [], []
    # fix page number - ensure to have ascending page numbers
    for page, (first, second) in enumerate(zip(left, right)):
        lresult.append(first._replace(page=page))  # pylint:disable=W0212
        rresult.append(second._replace(page=page))  # pylint:disable=W0212
    return lresult, rresult
