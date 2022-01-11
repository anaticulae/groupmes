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

import dataclasses

import configo
import iamraw
import texmex.navigator
import utila

import groupme.footer.strategy as gfs
import groupme.footer.strategy.pages as gfsp
import groupme.footnotes.highnote

FOOTNOTE_NUMBER_ERROR_MAX = configo.HV_FLOAT_PLUS(default=0.4)


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

    def result(self):
        pagenumber_locations = gfsp.pagenumber_location(
            self.horizontals,
            self.sizeandborders,
            self.pagenumbers,
            self.pagetextnavigators,
        )
        result = []
        for page in self.horizontals:
            sizeandborder = utila.select_page(
                self.sizeandborders,
                page.page,
            )
            pagetextnavigator = utila.select_page(
                self.pagetextnavigators,
                page.page,
            )
            pagenumber_location = utila.select_page(
                pagenumber_locations,
                page.page,
            )
            processed = process_page(
                pagenumber_location=pagenumber_location,
                horizontals=page.content,
                sizeandborder=sizeandborder,
                pagetextnavigator=pagetextnavigator,
                footnote_strategy=self.footnote_strategy,
                invalid_footer=self.invalid_footer,
            )
            if processed.footer is None and processed.header is None:
                continue
            result.append(processed)
        result = merge_footer_pages(result)
        if footnote_number_error(result):
            result = []
        return result

    def report(self) -> gfs.FooterStrategyResultReport:
        # TODO: Avoid multiple computation, require  concept.
        detected = self.result()
        detected = judge_detection(detected)
        report = analyze(detected)
        return report


@dataclasses.dataclass
class MovingFooterResultReport(gfs.FooterStrategyResultReport):  # pylint:disable=R0903
    footer: int = None
    header: int = None
    footer_empty: int = None
    too_many_empty_footer: bool = False


# relation between detected and empty detected footer to reduce miss detection
WRONG_STRATEGY_EMPTY_FOOTER_FACTOR = configo.HV_PERCENT_PLUS(default=20)

BOTTOM_BORDER = configo.HV_PERCENT_PLUS(default=60)


def process_page(
    pagenumber_location,
    horizontals,
    sizeandborder,
    pagetextnavigator,
    footnote_strategy: callable = None,
    invalid_footer: callable = None,
) -> iamraw.PageContentFooterHeader:
    pagenumber = pagetextnavigator.page
    pagewidth = sizeandborder.size.width
    pageheight = sizeandborder.size.height
    # check PAGENUMBR RAW? OR INHERIT FROM PTN?
    bottomed = select_footer_line(horizontals, pagewidth, pageheight)
    # this algo does not detect any header
    header = None
    # determine start of footer
    footer = None
    if bottomed is not None:
        footer = extract_footer(
            bottomed,
            pageheight,
            pagenumber_location,
            pagetextnavigator,
            footnote_strategy=footnote_strategy,
            invalid_footer=invalid_footer,
        )
    result = iamraw.PageContentFooterHeader(
        header=header,
        footer=footer,
        page=pagenumber,
    )
    return result


def select_footer_line(horizontals, pagewidth, pageheight) -> float:
    # TODO: USE MOST COMMON FOOTER DECIDER
    footer_start = pageheight * BOTTOM_BORDER
    # skip horizontals which are located too top
    filtered = [item for item in horizontals if item.box.y0 >= footer_start]
    # potential footer is located too right
    x0_max = groupme.footnotes.utils.FOOTNOTE_X0_MAX(pagewidth)
    filtered = [item for item in filtered if item.box.x0 <= x0_max]
    # determine y-level
    bottomed = max([item.box.y0 for item in filtered], default=None)
    return bottomed


def extract_footer(
    footerstart: float,
    pageheight: int,
    pagenumber_location,
    pagetextnavigator,
    footnote_strategy: callable = None,
    invalid_footer: callable = None,
) -> iamraw.MovingFooterInformation:
    if footnote_strategy is None:
        footnote_strategy = groupme.footnotes.highnote.parse
    begin = utila.roundme(footerstart / pageheight)
    # in the current parser state, the location of tiny distances between
    # objects is not interpreted correctly. The distance is often to small.
    # TODO: HOW TO HANDLE NON DETECTED PAGENUMBER_LOCATION
    end = pageheight
    if pagenumber_location and pagenumber_location.footer:
        end = pagenumber_location.footer.page_location.y0
    end = utila.roundme(end / pageheight)
    # TODO: USE TWO_THIRDS Strategy
    content = pagetextnavigator.between(
        begin,
        end,
        selector=texmex.navigator.SelectBounding.BOTTOM,
    )
    if invalid_footer and invalid_footer(begin, content):
        return None
    # splitted by highnotes
    footnotes = footnote_strategy(
        content=content,
        width=pagetextnavigator.width,
        pagenumber=pagetextnavigator.page,
    )
    if not footnotes:
        # no footnotes parsed, therefore do not return MovingFooterInformation
        return None
    footer = iamraw.MovingFooterInformation(
        begin=begin,
        end=end,
        notes=footnotes,
    )
    return footer


def footnote_number_error(footers: list) -> bool:
    numbers = []
    for footer in footers:
        for note in footer.footer.notes:
            if note.number is None:
                continue
            if not isinstance(note.number, int):
                utila.log(f'invalid footenumber: {note.number}')
                continue
            numbers.append(note.number)
    if len(numbers) < 2:
        return False
    diffed = utila.diffs(numbers)
    if not diffed:
        return False
    if len(diffed) == 1 and diffed[0] > 0:
        # [13, -1] for example
        return True
    fit, error = utila.partition(
        key=lambda x: 1 <= x <= 2,
        items=diffed,
    )
    if not error:
        return False
    error_rate = utila.rate_sum(error, fit)
    if error_rate > FOOTNOTE_NUMBER_ERROR_MAX:
        return True
    return False


def merge_footer_pages(footers):
    """Merge following uncompleted footnotes together."""
    # TODO: IMPROVE CHECK IF MERGING IS REQUIRED
    # TODO: MERGE MORE THAN TWO PAGES
    for current, after in zip(footers[0:-1], footers[1:]):
        if (after.page - current.page) != 1:
            # no page neighbours
            continue
        if not after.footer.notes:
            continue
        if not current.footer.notes:
            continue
        if current.footer.notes[-1].number == -1:
            # could not merge, I am not a valid footnote
            continue
        if after.footer.notes[0].number not in (-1, None):
            # no merge required, footnote have a number
            continue
        # merge notes together
        current.footer.notes[-1] = iamraw.FootNoteMerged(
            page=current.footer.notes[-1].page,
            number=current.footer.notes[-1].number,
            notes=[
                current.footer.notes[-1],
                after.footer.notes[0],
            ],
        )
        #update bounding
        # TODO: UPDATE PAGE BOUNDING OVER TWO PAGES MAKES NO SENCE?
        # current.footer.notes[-1].bounding = utila.rectangle_max(
        #     [item.bounding for item in current.footer[-1].notes])
        # remove merged notes from after
        after.footer.notes = after.footer.notes[1:]
    return footers


def analyze(results) -> MovingFooterResultReport:
    footer_count = gfs.count_footer(results)
    emptyfooter_count = count_empty(results)
    empty_factor = emptyfooter_count / footer_count if footer_count else 0
    too_many_empty_footer = empty_factor >= WRONG_STRATEGY_EMPTY_FOOTER_FACTOR
    # create report
    result = MovingFooterResultReport(
        footer=footer_count,
        footer_empty=emptyfooter_count,
        too_many_empty_footer=too_many_empty_footer,
    )
    return result


def count_empty(items: iamraw.PageContentFooterHeader) -> int:
    """Count `MovingFooterInformation` which contain a empty `notes` list"""
    footers = [item.footer for item in items if item.footer]
    empty_footnotes = [item for item in footers if not item.notes]
    result = len(empty_footnotes)
    return result


def judge_detection(items):
    """Second analyzing step. Prove that `items` contain a good
    detection result.

    The following things will be checked:

    - (x) selection of correct strategy
    - ( ) quality of extracted footnotes
    """
    report = analyze(items)
    # This can happen when using the wrong strategy. If we parse
    # FixedFooter with MovingFooterStrategy, there are a lot of footer
    # which are threated as MovingFooter with Footnote, but this detection
    # is not correct.
    if report.too_many_empty_footer:
        return []
    return items
