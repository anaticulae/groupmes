# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Footer Header Extraction Step
=============================

TODO:
    what should we do with empty header/footer
"""

import collections
import typing

import iamraw
import serializeraw
import texmex
import utila

import groupme.feature.pagenumbers
import groupme.footer
import groupme.footer.strategy
import groupme.footer.strategy.common
import groupme.footer.strategy.fixed
import groupme.footer.strategy.moving
import groupme.footer.strategy.pages


def work(
    text: str,
    text_positions: str,
    fontheader: str,
    fontcontent: str,
    horizontals: str,
    sizeandborders: str,
    pagenumber: str,
    pages=None,
) -> str:
    """Extract footer and header area out of horizontal lines

    Returns:
        Dumped list with top and bottom border, which separates the
        content from the footer and or header, for every page
    """
    utila.call('footer')
    # load
    horizontals = serializeraw.load_horizontals(horizontals, pages=pages)
    sizeandborders = serializeraw.load_pageborders(sizeandborders, pages=pages)
    pagenumber = serializeraw.load_pagenumbers(pagenumber, pages=pages)
    ptns = serializeraw.create_pagetextnavigators_fromfile(
        text,
        text_positions,
        fontheader,
        fontcontent,
        pages=pages,
    )
    ptns = groupme.feature.pagenumbers.rotate_ifrequired(ptns, sizeandborders)
    # work
    result = extract_footerheader(
        horizontals=horizontals,
        sizeandborders=sizeandborders,
        pagenumbers=pagenumber,
        pagetextnavigators=ptns,
    )
    validate(result)
    # dump
    dumped = serializeraw.dump_headerfooter(result)
    return dumped


def extract_footerheader(
    horizontals: iamraw.PagesWithHorizontalList,
    sizeandborders: iamraw.PageSizeBorderList,
    pagenumbers,
    pagetextnavigators: texmex.PageTextNavigators,
) -> iamraw.PageContentFooterHeaders:
    """Extract most common header/footer of the document

    Returns:
        The most common header/foooter combination for the document
    """
    strategies = groupme.footer.strategies()
    results = [
        strategy(
            horizontals=horizontals,
            sizeandborders=sizeandborders,
            pagenumbers=pagenumbers,
            pagetextnavigators=pagetextnavigators,
        ).result() for strategy in strategies
    ]
    result = judge_strategy(results)
    return result


def judge_strategy(
    results: typing.List[iamraw.PageContentFooterHeaders],
) -> iamraw.PageContentFooterHeaders:
    """Decide which results fits best.

    Zip result of different strategies. Sometimes there are multiple
    options, therefore we have to use the priorities below.

    Sources/Concept:

        - MovingFooter:                footer (first prio)
        - Pages:                       footer (second prio)
        - FixedFooter:      header and footer (third prio)
        - Common:           header            (last prio)
        - PlainMoving:

    Args:
        results: lists of `groupme.footer.FooterHeaderDetectionStrategy`.result
    Returns:
        list of zipped result
    """
    assert results is not None, 'require list of strategy results'
    qualities = quality(results)
    result = []
    for pagenumber, (
            common,
            fixed,
            moving,
            pages,
            plainmoving,
    ) in utila.sync_pages(results):
        header = fixed.header if fixed else None
        footer = fixed.footer if fixed else None

        if pages and pages.footer:
            footer = pages.footer

        if moving and moving.footer and moving.footer.notes:
            footer = moving.footer

        if common and common.header:
            if not header:
                header = common.header
            elif qualities[0] == max(qualities):
                # compare quality of both extractions
                # TODO: MORE THAN ONE EXTRACTION CAN HAVE BEST
                # EXTRACTION QUALITY.
                header = common.header

        if not (moving and moving.footer) and plainmoving and plainmoving.footer: # yapf:disable
            # use plain moving only if no other strategy works
            footer = plainmoving.footer

        current = iamraw.PageContentFooterHeader(
            header=header,
            footer=footer,
            page=pagenumber,
        )
        result.append(current)

    page_order = [item.page for item in result]
    assert utila.isascending(page_order), page_order
    return result


def quality(results: list) -> tuple:
    """Determine quality[0.0, 1.0] of every extraction strategy."""
    # count number of page
    pages = set()
    # count result for every strategy
    counter = collections.defaultdict(int)
    for pagenumber, data in utila.sync_pages(results):
        pages.add(pagenumber)
        for index, item in enumerate(data):
            if not item:
                continue
            counter[index] += 1

    result = tuple(counter[index] / len(pages) if pages else 0
                   for index, _ in enumerate(results))
    return result


def validate(items: list):
    """Validate list of pageable items. If some `page` attribute is
    duplicated, raise ValueError.

    Args:
        items(list): list of objects with <page,content>
    Raises:
        ValueError: if some page attribute is duplicated.
    """
    # TODO: REMOVE AFTER UPGRADING IAMRAW
    counter = collections.Counter()
    for item in items:
        counter[item.page] += 1
    msg = []
    for page, value in counter.most_common():
        if value <= 1:
            continue
        msg.append(f'duplicated page: {page} ({value})')
    if msg:
        raise ValueError(utila.NEWLINE.join(msg))
