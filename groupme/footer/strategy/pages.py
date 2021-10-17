# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""This strategy aims to detect footer which contains only a page number
and distance to text before.

Example:

- docu/howto_argparse.pdf
- technical/page_24_color_figures_images.pdf

Extract page numbers as footer if the distance between page number and
next horizontal line is greater than `DISTANCE_TO_HORIZONTAL_MIN`.

"""

import configo
import iamraw
import texmex
import utila

import groupme.footer.strategy as gfs

DISTANCE_TO_HORIZONTAL_MIN = configo.HV_INT_PLUS(default=15, limit=250)

PAGE_NUMBER_Y_MAX = configo.HV_FLOAT_PLUS(default=250.0)


class PageNumberStrategy(gfs.FooterHeaderDetectionStrategy):

    def result(self):
        result = []
        if isinstance(self.pagenumbers, tuple):
            assert len(self.pagenumbers) == 2, 'require left and right pages'
            left = self.process_pageside(self.pagenumbers[0])
            right = self.process_pageside(self.pagenumbers[1])
            result.extend(left)
            result.extend(right)
            # order pages by pdf raw page, this is required of merging
            # left and right side
            result = sorted(result, key=lambda item: item.page)
        else:
            result = self.process_pageside(self.pagenumbers)
        return result

    def process_pageside(self, pagenumbers):
        result = []
        pagenumbers = {item[0]: (item[1], item[2]) for item in pagenumbers}
        for pdfpage, rawpage in pagenumbers.items():
            pageheight = self.pageheight(pdfpage)
            assert pageheight > 0, f'invalid pageheight: {pageheight}'
            horizontals = utila.select_page(self.horizontals, pdfpage)
            navigator = utila.select_page(self.pagetextnavigators, pdfpage)

            processed = process_page(pdfpage, rawpage, horizontals)
            if processed is None:
                continue
            _, location = processed
            header, footer = None, None
            # TODO: CHECK ROTATED PAGES
            if location[3] < PAGE_NUMBER_Y_MAX:
                # header
                header = create_headerinformation(
                    location,
                    navigator,
                    pageheight,
                    rawpage,
                )
            else:
                # footer
                footer = create_footerinformation(
                    location,
                    navigator,
                    pageheight,
                    rawpage,
                )
            footer_header = iamraw.PageContentFooterHeader(
                header=header,
                footer=footer,
                page=pdfpage,
            )
            result.append(footer_header)
        return result

    def report(self) -> gfs.FooterStrategyResultReport:
        pass


# plus 1 percent off to ensure that content and header is separated correctly.
HEADER_TOL = configo.HV_FLOAT_PLUS(default=0.01)


def create_headerinformation(
    location,
    navigator,
    pageheight,
    rawpage,
) -> iamraw.PagesFooterInformation:
    # footer detection
    bounding = location
    begin = texmex.START
    end = bounding.y1 / pageheight
    end = utila.roundme(HEADER_TOL + end)
    raw = navigator.find(bounding).text.strip()
    result = iamraw.PagesFooterInformation(
        begin=begin,
        end=end,
        page_location=bounding,
        page=iamraw.PageInformation(value=rawpage[1], raw=raw),
    )
    return result


def create_footerinformation(
    location,
    navigator,
    pageheight,
    rawpage,
) -> iamraw.PagesFooterInformation:
    # footer detection
    bounding = location
    begin = utila.roundme(bounding.y0 / pageheight)
    end = texmex.END
    raw = navigator.find(bounding).text.strip()
    result = iamraw.PagesFooterInformation(
        begin=begin,
        end=end,
        page_location=bounding,
        page=iamraw.PageInformation(value=rawpage[1], raw=raw),
    )
    return result


def process_page(page, rawpage, horizontals):
    if rawpage is None:
        return None
    pagenumber_bounding = rawpage[0]
    distance_to_firsthorizontal = distance(pagenumber_bounding, horizontals)
    if distance_to_firsthorizontal <= DISTANCE_TO_HORIZONTAL_MIN:
        # Require some distance to horizontal line
        # TODO: ADD DOCU HERE
        return None
    return (page, pagenumber_bounding)


def distance(bounding, items):
    items = items.content if items else []
    ydistance = [rectangle_distance_y(bounding, item.box) for item in items]
    if not ydistance:
        return utila.INF
    result = min(ydistance)
    result = utila.roundme(result)
    return result


def rectangle_distance_y(first, second) -> float:
    firsty = (first[1] + first[3]) / 2
    secondy = (second[1] + second[3]) / 2
    return abs(firsty - secondy)


def pagenumber_location(
    horizontals,
    sizeandborders,
    pagenumbers,
    pagetextnavigators,
):
    strategy = PageNumberStrategy(
        horizontals,
        sizeandborders,
        pagenumbers,
        pagetextnavigators,
    )
    result = strategy.result()
    return result
