# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Page Numbers Extraction Step
============================

Start working on footer extractor.

Required resources:

    # PageSize
    # HorizontalLines
    # Text annotated with location

Required API:

    # before/ after method to determine items
"""

import collections
import typing

import elements
import iamraw
import serializeraw
import texmex
import utila

PageContentTextPosition = collections.namedtuple(
    'PageContentTextPosition',
    'content, page',
)

# TODO: REPLACE HOLY VALUE
TOP_BORDER = 0.2  # Header in the range of 0% till 20%
TOP_MAX_DIFFERENCE = 20.0

# TODO: Think about scaling this value depending on result
BOTTOM_BORDER = 0.8  # Footer is in range of 80% till 100%
BOTTOM_MAX_DIFFERENCE = 20.0
BOTTOM_MAX_AREA = 2500.0  # page number is not very big

PAGE_ELEMENTS_MIN = 4


def work(text: str, textpositions: str, pages: tuple = None) -> str:
    utila.call('numbers')
    navigators = serializeraw.create_pagetextnavigators_fromfile(
        text=text,
        textpositions=textpositions,
        pages=pages,
    )
    pagenumbers = determine_pagenumbers(navigators)
    dumped = serializeraw.dump_pagenumbers(pagenumbers)
    return dumped


def determine_pagenumbers(navigators):
    rotated, normal = utila.partition(isrotated, navigators)
    detected = header(normal) + footer(normal)
    return pagenumbers(detected)


def header(
    navigators,
    *,
    numbers_only: bool = True,
    remove_empty: bool = True,
) -> list:
    collected = [(page.page, page.before(TOP_BORDER)) for page in navigators]
    common = valid_content(
        collected,
        numbers_only=numbers_only,
        remove_empty=remove_empty,
    )
    return common


def footer(
    navigators,
    *,
    numbers_only: bool = True,
    remove_empty: bool = True,
) -> list:
    """Detect similar elements in footer area which are duplicated on
    different pages.

    Args:
        navigators(list): list of text navgiators
        numbers_only(bool): if True, remove all non numeric/romanic elements
        remove_empty(bool): remove empty elements, e.g. whitespaces
    Returns:
        A list of clustered page footer content which are expected of
        beeing the page numbers.
    """
    collected = [(page.page, page.after(BOTTOM_BORDER)) for page in navigators]
    common = valid_content(
        collected,
        numbers_only=numbers_only,
        remove_empty=remove_empty,
    )
    return common


def valid_content(
    navigators,
    max_area: float = BOTTOM_MAX_AREA,
    max_difference: float = BOTTOM_MAX_DIFFERENCE,
    min_elements: int = PAGE_ELEMENTS_MIN,
    numbers_only: bool = True,
    remove_empty: bool = True,
):
    """Detect similar elements which are duplicated on different pages."""
    filtered = []
    for pagenumber, footercontent in navigators:
        pagecontent = []
        for item in footercontent:
            text = item.text.strip()
            if utila.rectangle_size(item.bounding) > max_area:
                # ignore to big items
                continue
            if remove_empty and not text:
                # filter empty items
                continue
            if numbers_only and not elements.ispagenumber(text):
                # remove non numeric items
                continue
            # support -1-, -2-, ...
            clean_number = text.replace('-', '', 2).strip()
            # 32/54
            clean_number = clean_number.split('/')[0]
            # TODO: DELIVER RAW DATA FOR FOOTER PAGES STRATEGY DETECTION
            item = (item.bounding, clean_number, pagenumber)
            pagecontent.append(item)
        filtered.append(pagecontent)
    common = utila.common_items(
        filtered,
        max_difference=max_difference,
        min_elements=min_elements,
    )
    return common


def isrotated(navigator) -> bool:
    return navigator.width > navigator.height


def isrightpage(pdf_pagenumber: int) -> bool:
    """What pdf page is the left side?
    The first page is the right page? """
    pdf_pagenumber = int(pdf_pagenumber)
    return pdf_pagenumber % 2 == 0


Cluster = typing.List[typing.Tuple[iamraw.BoundingBox, str]]


def pagenumbers(clusters: typing.List[Cluster]) -> list:
    """Determine pagenumbers out of list of cluster

    2. Scenarios are possible, we have alternating left and right page numbers
    or the page numbers are only on one possition.

    Args:
        clusters: List of cluster -> List[List[(boundingbox, content)]]
    Returns:
        singlepage or (left, right)
    """
    left, right = [], []
    for clusterid, cluster in enumerate(clusters):
        for _, (bounding, content, pdfpage) in cluster:
            content = str(content)
            if not elements.ispagenumber(content):
                continue
            try:
                content = int(content)  # pylint:disable=R0204
            except ValueError:
                # roman number
                pass
            # save number as tuple of pdf_page and detected page
            item = (pdfpage, bounding, content)
            if isrightpage(pdfpage):
                right.append(item)
            else:
                left.append(item)
    if morethanone(clusters):
        # TODO: INTRODUCE MORE THAN, LEFT, RIGHT ETC.
        return left, right
    # One cluster is used, we do not have right and left pagenumber
    singlepage = left + right
    # Sort by pdfpage
    singlepage = sorted(singlepage, key=lambda number: number[0])
    return singlepage


def morethanone(clusters) -> bool:
    """Determine vector to position of detected page numbers.

    If this maxdistance/diff is higher than a threshold, we have left
    and right page numbers.
    """
    collected = []
    for cluster in clusters:
        for _, item in cluster:
            centered = rectangle_center(item[0])
            length = utila.length(*(0, 0, centered[0], centered[1]))
            collected.append(length)
    collected = utila.make_unique(collected)
    if not collected:
        return False
    mins, maxs = utila.mins(collected), utila.maxs(collected)
    diff = maxs - mins
    result = diff > 100  # HOLY VALUE
    return result


def rectangle_center(rectangle) -> tuple:
    # TODO: MOVE TO UTILA
    x = (rectangle[0] + rectangle[2]) / 2
    y = (rectangle[1] + rectangle[3]) / 2
    return utila.roundme((x, y))
