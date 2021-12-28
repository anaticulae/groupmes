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

COMMON_HEADER_ERROR_MAX = configo.HV_FLOAT_PLUS(default=10.0)
# minimal items in a cluster to be detected and accepted as feature.
OCCURRENCE_MIN = configo.HolyTable(
    items=(
        (0, 5),
        (10, 5),
        (15, 8),
        (30, 12),
        (50, 14),
        (100, 25),
    ),
    right_outranges_none=False,
)

TOP_AREA = configo.HV_PERCENT_PLUS(default=15)


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
    result = items[0]
    value = count_empty(result)
    for current in items[1:]:
        wholes = count_empty(current)
        if wholes is None:
            # nothing to count
            continue
        if wholes >= value:
            # worser than current result
            continue
        # better
        result = current
        value = wholes
    return result


# count holes in [20%,80%]
COUNT_EMPTY_DOCUMENT_PAGE_START = configo.HV_PERCENT_PLUS(default=20)

COUNT_EMPTY_DOCUMENT_PAGE_END = configo.HV_PERCENT_PLUS(default=80)


def count_empty(collected) -> int:
    # count holes in [20%,80%]
    if not collected:
        return None
    # skip start and end of document cause we expect a lot of
    # empty/skipped header.
    start = int(len(collected) * COUNT_EMPTY_DOCUMENT_PAGE_START)
    end = int(len(collected) * COUNT_EMPTY_DOCUMENT_PAGE_END)
    empty = [
        item for item in collected[start:end]
        if not item[1].title and not item[1].undefined
    ]
    return len(empty)


# plus 1 percent off to ensure that content and header is separated correctly.
HEADER_TOL = configo.HV_FLOAT_PLUS(default=0.01)


def cluster_pages(
    pagenavigators: texmex.PageTextNavigators,
    tryagain: bool = False,
):
    occurrence_min = HEADER_TEXT_OCCURENCE_MIN
    if tryagain:
        # run algorithmn with lower bound to gather more data but may be
        # more instable.
        occurrence_min = HEADER_TEXT_OCCURENCE_TRYAGAIN_MIN
    # prepare data
    with_box = utila.flatten(
        prepare_clustering(
            pagenavigators,
            occurrence_min=occurrence_min,
        ))
    pagenumbers = len(pagenavigators)
    min_cluster_count = OCCURRENCE_MIN(pagenumbers)
    # TODO: REMOVE LATER, SWITCH TABLE BASED ENTROPY OF POTENTIAL HEADER AREA?
    min_cluster_count = 5
    clusters = utila.three_side_equal_cluster(  # pylint:disable=E1123
        todo=with_box,
        max_diff=COMMON_HEADER_ERROR_MAX,
        min_elements=min_cluster_count,
    )
    if not clusters:
        return []
    grouped = {}
    for cluster in clusters:
        for bounding, text, pageheight, pagenumber in cluster:
            end = bounding.y1 / pageheight
            end = utila.roundme(HEADER_TOL + end)
            current = grouped.get(pagenumber, None)
            current = create_fixedheader(current, text.text, pagenumber, end)
            grouped[pagenumber] = current
    result = list(grouped.items())
    # sort FixedHeaderInformation by page
    result.sort(key=lambda x: x[0])
    return result


def create_fixedheader(
    current,
    text: str,
    pagenumber,
    end,
) -> iamraw.FixedHeaderInformation:
    # remove newline at end TODO: REMOVE LATER
    text = text.strip()
    if current is None:
        current = iamraw.FixedHeaderInformation(
            begin=texmex.START,
            end=end,
            page=iamraw.PageInformation(value=pagenumber, raw=None),
        )
    title = groupme.footer.headnotes.parse_title(text)
    if title:
        current.title = title
        return current
    parsed = groupme.footer.headnotes.parse_pagenumber(text)
    if parsed:
        current.page = parsed
        return current
    current.undefined.append(iamraw.RawText(text=text))
    return current


HEADER_TEXT_OCCURENCE_MIN = configo.HV_INT_PLUS(default=5)

HEADER_TEXT_OCCURENCE_TRYAGAIN_MIN = configo.HV_INT_PLUS(default=3)


def prepare_clustering(
    pagetextnavigators,
    occurrence_min: int = HEADER_TEXT_OCCURENCE_MIN,
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


def header_content(pagecontents, occurrence_min: int) -> set:
    """Some documents does not have any header, but equal sized first line(s).

    We have to ignore these first content lines.
    """
    collected = collections.defaultdict(int)
    for pagecontent in pagecontents:
        for item in pagecontent:
            text = item[1].text.strip()
            collected[text] += 1
    # sum textual equal as equal items
    # 6.3 evaluation 106
    # 6.3 evaluation 107
    # 6.3 evaluation 108
    # HINT: if layout is better parsed page numbers are may not included
    maxdiff = 0.8  # TODO: HOLY VALUE
    counted = {
        key: sum([
            val for current, val in collected.items()
            if utila.similar(expected=key, current=current, maxdiff=maxdiff)
        ]) for key in collected.keys()
    }
    valid = {key for key in collected.keys() if counted[key] >= occurrence_min}
    return valid
