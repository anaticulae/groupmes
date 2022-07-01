# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Moving Footer Extraction Step
=============================

Requirements:
    We do not check the header, because it is required, that this header
    is fixed.

Example:

- master/page_72_noimages_toc.pdf
- bachelor/page_111_images_toc.pdf

TODO: Think about header
"""

import iamraw
import texmex.navigator
import utila

import groupme.footer.strategy as gfs
import groupme.footer.strategy.moving.finish as gfsmf
import groupme.footer.strategy.moving.judge as gfsmj
import groupme.footer.strategy.moving.separator as gfsms
import groupme.footer.strategy.pages as gfsp
import groupme.footnotes.strategy.highnote


class MovingFooterStrategy(gfs.FooterHeaderDetectionStrategy):

    def __init__(
        self,
        horizontals: iamraw.PagesWithHorizontalList,
        sizeandborders: iamraw.PageSizeBorderList,
        pagenumbers,
        pagetextnavigators: texmex.PageTextNavigators,
        footnote_strategy: callable = None,
        invalid_footer: callable = None,
    ):
        super().__init__(
            horizontals,
            sizeandborders,
            pagenumbers,
            pagetextnavigators,
        )
        self.footnote_strategy = footnote_strategy
        self.invalid_footer = invalid_footer

    def run(self):
        pagenumber_locations = gfsp.pagenumber_location(
            self.horizontals,
            self.sizeandborders,
            self.pagenumbers,
            self.pagetextnavigators,
        )
        horizontals = gfsms.footer_separator(self.horizontals, self.pagesize)
        pages = utila.SelectPage(
            sizeandborders=self.sizeandborders,
            ptns=self.pagetextnavigators,
            pagenumber_locations=pagenumber_locations,
        )
        result = []
        for horizontal in horizontals:
            sizeborder, ptn, pagenumber_box = pages.getpage(horizontal.page)
            processed = process_page(
                pagenumber_location=pagenumber_box,
                horizontals=horizontal.content,
                sizeandborder=sizeborder,
                ptn=ptn,
                footnote_strategy=self.footnote_strategy,
                invalid_footer=self.invalid_footer,
            )
            if processed.footer is None and processed.header is None:
                continue
            result.append(processed)
        return result

    def pagesize(self, pagenumber):
        selected = utila.select_page(
            self.sizeandborders,
            page=pagenumber,
        )
        if selected is None:
            return (595.28, 841.89)
        return (selected.size.width, selected.size.height)

    def result(self):
        detected = self.run()
        utila.verbose('footer before merge:')
        utila.verbose(detected)
        utila.verbose()
        result = gfsmf.merge_footer_pages(detected)
        utila.verbose('footer after merge:')
        utila.verbose(result)
        utila.verbose()
        result = gfsmj.last(result)
        utila.verbose('footer after last:')
        utila.verbose(result)
        utila.verbose()
        return result

    def report(self) -> gfs.FooterStrategyReport:
        # TODO: Avoid multiple computation, require  concept.
        detected = self.result()
        result = gfsmj.report(detected)
        return result


def process_page(
    pagenumber_location,
    horizontals,
    sizeandborder,
    ptn,
    footnote_strategy: callable = None,
    invalid_footer: callable = None,
) -> iamraw.PageContentFooterHeader:
    pagesize = sizeandborder.size
    # determine start of footer
    footer = None
    # check PAGENUMBR RAW? OR INHERIT FROM PTN?
    bottomed = gfsms.select_footer_line(
        horizontals,
        pagewidth=pagesize.width,
        pageheight=pagesize.height,
    )
    if bottomed is not None:
        footer = extract_footer(
            bottomed,
            pageheight=pagesize.height,
            pagenumber_location=pagenumber_location,
            ptn=ptn,
            footnote_strategy=footnote_strategy,
            invalid_footer=invalid_footer,
        )
    # this algo does not detect any header
    header = None
    result = iamraw.PageContentFooterHeader(
        header=header,
        footer=footer,
        page=ptn.page,
    )
    return result


def extract_footer(
    footerstart: float,
    pageheight: int,
    pagenumber_location,
    ptn,
    footnote_strategy: callable = None,
    invalid_footer: callable = None,
) -> iamraw.MovingFooterInformation:
    if footnote_strategy is None:
        footnote_strategy = groupme.footnotes.strategy.highnote.parse
    begin = utila.roundme(footerstart / pageheight)
    # in the current parser state, the location of tiny distances between
    # objects is not interpreted correctly. The distance is often to small.
    # TODO: HOW TO HANDLE NON DETECTED PAGENUMBER_LOCATION
    end = pageheight
    if pagenumber_location and pagenumber_location.footer:
        end = pagenumber_location.footer.page_location.y0
    end = utila.roundme(end / pageheight)
    # TODO: USE TWO_THIRDS Strategy
    content = ptn.between(
        begin,
        end,
        selector=texmex.navigator.SelectBounding.BOTTOM,
    )
    if invalid_footer and invalid_footer(begin, content):
        utila.debug(f'invalid footer on page {ptn.page}: {content}')
        return None
    # splitted by highnotes
    footnotes = footnote_strategy(
        content=content,
        width=ptn.width,
        pagenumber=ptn.page,
    )
    if nonumber(footnotes):
        return None
    if not footnotes:
        # no footnotes parsed, therefore do not return MovingFooterInformation
        return None
    footer = iamraw.MovingFooterInformation(
        begin=begin,
        end=end,
        notes=footnotes,
    )
    return footer


NONUMBER = (-1, '-1')


def nonumber(footnotes) -> bool:
    if not footnotes:
        return False
    counted = len([item for item in footnotes if item.number in NONUMBER])
    if not counted:
        return False
    if counted >= 2:
        return True
    return False
