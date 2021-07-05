# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""common text strategy
====================

The ``common text strategy`` extracts header or footer based on common
text and images. There is no horizontal line required.

.. note ::
    TODO: SUPPORT COMMON IMAGES
"""

import collections

import configo
import elements
import iamraw
import texmex
import utila

import groupme.footer.headnotes
import groupme.footer.strategy as gfs

COMMON_HEADER_MAX_ERROR = 10.0  # TODO: HOLY VALUE
# minimal items in a cluster to be detected and accepted as feature.
MIN_OCCURRENCE = configo.HolyTable(
    items=(
        (0, 5),
        (10, 7),
        (15, 10),
        (30, 15),
        (50, 20),
        (100, 25),
    ),
    right_outranges_none=False,
)

TOP_AREA = 0.15  # TODO: HOLY VALUE


class CommonTextStrategy(gfs.FooterHeaderDetectionStrategy):  # pylint:disable=W0223

    def result(self):
        header = cluster_pages(self.pagetextnavigators)
        header_again = cluster_pages(self.pagetextnavigators, tryagain=True)
        if header:
            header = best(header, header_again)
        result = [
            iamraw.PageContentFooterHeader(
                header=header,
                footer=None,
                page=page,
            ) for (page, header) in header
        ]
        return result


def best(*items):

    def empty(collected) -> int:
        # select hole in [20%,80%]
        if not collected:
            return None
        # skip start and end of document cause we expect a lot of
        # empty/skipped header.
        start, end = int(len(collected) * 0.2), int(len(collected) * 0.8)
        empty = [
            item for item in collected[start:end]
            if not item[1].title and not item[1].undefined
        ]
        return len(empty)

    result = items[0]
    value = empty(result)

    for current in items[1:]:
        wholes = empty(current)
        if wholes is None:
            continue
        if wholes >= value:
            continue
        # better
        result = current
        value = wholes
    return result


# plus 1 percent off to ensure that content and header is separated correctly.
HEADER_TOL = configo.HV_FLOAT_PLUS(default=0.01)


def cluster_pages(
    pagenavigators: texmex.PageTextNavigators,
    tryagain: bool = False,
):
    pagenumbers = len(pagenavigators)
    min_cluster_count = MIN_OCCURRENCE(pagenumbers)
    occurrence_min = MIN_HEADER_TEXT_OCCURENCE
    if tryagain:
        # run algorithmn with lower bound to gather more data but may be
        # more instable.
        occurrence_min = MIN_HEADER_TEXT_OCCURENCE_TRYAGAIN
    # prepare data
    with_box = utila.flatten(
        prepare_clustering(
            pagenavigators,
            occurrence_min=occurrence_min,
        ))
    clusters = utila.three_side_equal_cluster(  # pylint:disable=E1123
        todo=with_box,
        max_diff=COMMON_HEADER_MAX_ERROR,
        min_elements=min_cluster_count,
    )
    if not clusters:
        return []
    grouped = {}
    for cluster in clusters:
        for bounding, text, pageheight, pagenumber in cluster:
            end = utila.roundme(bounding.y1 / pageheight)
            end = HEADER_TOL + end
            create_fixedheader(grouped, text.text, pagenumber, end)
    result = list(grouped.items())
    # sort FixedHeaderInformation by page
    result.sort(key=lambda x: x[0])
    return result


def create_fixedheader(collected, text: str, pagenumber, end):
    # remove newline at end TODO: REMOVE LATER
    text = text.strip()
    try:
        current = collected[pagenumber]
    except KeyError:
        current = iamraw.FixedHeaderInformation(
            begin=texmex.START,
            end=end,
            page=iamraw.PageInformation(value=pagenumber, raw=None),
        )
        collected[pagenumber] = current
    title = groupme.footer.headnotes.parse_title(text)
    if title:
        current.title = title
        return
    pagenumber = groupme.footer.headnotes.parse_pagenumber(text)
    if pagenumber:
        current.page = pagenumber
        return
    current.undefined.append(iamraw.RawText(text=text))


MIN_HEADER_TEXT_OCCURENCE = 5  # TODO: HOLY VALUE
MIN_HEADER_TEXT_OCCURENCE_TRYAGAIN = 3  # TODO: HOLY VALUE


def prepare_clustering(
    pagetextnavigators,
    occurrence_min: int = MIN_HEADER_TEXT_OCCURENCE,
):
    collected = []
    for page in pagetextnavigators:
        content = [(
            item.bounding,
            item,
            page.height,
            page.page,
        ) for item in page.before(TOP_AREA)]
        collected.append(content)
    valid = header_content(collected, occurrence_min=occurrence_min)
    result = []
    for page in collected:
        content = [
            item for item in page if item[1].text.strip() in valid or
            elements.ispagenumber(item[1].text)
        ]
        result.append(content)
    return result


def header_content(clusters, occurrence_min: int) -> set:
    """Some documents does not have any header, but equal sized first line(s).

    We have to ignore this first content lines."""
    collected = collections.defaultdict(int)
    for cluster in clusters:
        for item in cluster:
            text = item[1].text.strip()
            collected[text] += 1
    valid = {key for key, value in collected.items() if value >= occurrence_min}
    return valid
