# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import texmex
import utila

import groupme.toc.group
import groupme.toc.strategy.regex

MIN_HEADLINE_SIZE = configo.HV_FLOAT_PLUS(15.0).value


def select_contentpages(
    textnavigators: texmex.PageTextNavigators,
    wrong_table=None,
    strategy: callable = None,
    skip_higherqual_level_three: bool = True,
    min_valid_lines_perpage=None,
) -> utila.Ints:
    """Use simple approach to decide which page contains table content."""
    if strategy is None:
        strategy = groupme.toc.strategy.regex.parse_page
    selected = []
    for page in textnavigators:
        firstheadline = headline(page)
        if firstheadline is not None and firstheadline in wrong_table:
            # This approach works only forward and not backwards.
            # TODO: WHAT SHOULD WE DO WHEN BOTH ARE ON THE SAME PAGE?
            continue
        utila.debug(f'page: {page.page}')
        current_page = strategy(page)
        if not current_page:
            utila.debug(f'could not parse any valid line on page: {page.page}')
            continue
        pageslines = texmex.count_textlines(page, remove_empty=True)
        if not pageslines:
            continue
        matched_percent = len(current_page) / pageslines
        utila.info(f'page percent: {matched_percent} on page: {page.page}')
        if min_valid_lines_perpage is not None and matched_percent < min_valid_lines_perpage:
            # avoid missdetection in random pages if only few lines are
            # missdetected as toc line.
            continue
        # TODO: group.level fails on failing level
        if skip_higherqual_level_three:
            level3 = [
                groupme.toc.group.level(item.level) for item in current_page
            ]
            level3 = [
                item for item in level3
                if item and isinstance(item.value, int) and item.value >= 3
            ]
            if any(level3):
                # TODO: THINK ABOUT THIS
                # level is mostly a table of content level
                continue
        selected.append(page.page)
    selected = sorted(utila.make_unique(selected))
    # select biggest connected chunck
    if selected:
        selected = utila.groupby_diff(selected, maxdiff=1)
        selected = utila.longest(selected)
    return selected


def headline(page):
    result = []
    for item in page:
        parsed = groupme.toc.strategy.regex.parse(item.text)
        if parsed:
            continue
        # most item is more robust than max item
        textsize = item.style.textsize()
        if textsize < MIN_HEADLINE_SIZE:
            continue
        result.append(item.text.strip())
    if not result:
        return None
    if len(result) > 1:
        return None
    return result[0]
