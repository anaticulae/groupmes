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

        result = [
            iamraw.PageContentFooterHeader(
                header=header,
                footer=None,
                page=page,
            ) for (page, header) in header
        ]
        return result


def cluster_pages(pagenavigators):
    pagenumbers = len(pagenavigators)
    min_cluster_count = MIN_OCCURRENCE(pagenumbers)

    with_box = utila.flatten(prepare_clustering(pagenavigators))

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


def prepare_clustering(pagetextnavigators):
    collected = []
    for page in pagetextnavigators:
        content = [(
            item.bounding,
            item,
            page.height,
            page.page,
        ) for item in page.before(TOP_AREA)]
        collected.append(content)
    valid = header_content(collected)
    result = []
    for page in collected:
        content = [
            item for item in page if item[1].text.strip() in valid or
            elements.ispagenumber(item[1].text)
        ]
        result.append(content)
    return result


MIN_HEADER_TEXT_OCCURENCE = 5  # TODO: HOLY VALUE


def header_content(clusters) -> set:
    """Some documents does not have any header, but equal sized first
    line(s). We have to ignore this first content lines."""
    collected = collections.defaultdict(int)
    for cluster in clusters:
        for item in cluster:
            text = item[1].text.strip()
            collected[text] += 1
    valid = {
        key for key, value in collected.items()
        if value >= MIN_HEADER_TEXT_OCCURENCE
    }
    return valid
