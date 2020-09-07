# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import texmex
import utila

import groupme.toc.group
import groupme.toc.strategy.regex


def select_contentpages(
        textnavigators: texmex.PageTextNavigators,
        wrong_table=None,
        strategy: callable = None,
        skip_higherqual_level_three: bool = True,
        min_valid_lines_perpage=None,
) -> utila.Ints:
    """Use simple approach to decide which page is a figure table page."""
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
        figurepage = strategy(page)
        if not figurepage:
            utila.debug(f'could not parse any figure line on page: {page.page}')
            continue
        pageslines = texmex.count_textlines(page, remove_empty=True)
        if not pageslines:
            continue
        figure_percent = len(figurepage) / pageslines
        utila.info(f'toc percent: {figure_percent} on page: {page.page}')
        if min_valid_lines_perpage is not None and figure_percent < min_valid_lines_perpage:
            # avoid missdetection in random pages if only few lines are
            # missdetected as toc line.
            continue
        # TODO: group.level fails on failing level
        if skip_higherqual_level_three:
            level3 = [
                groupme.toc.group.level(item.level) for item in figurepage
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
        selected = utila.groupby_diff(selected, diff=1)
        selected = utila.longest(selected)
    return selected


def headline(page):
    result = []
    for item in page:
        parsed = groupme.toc.strategy.regex.parse(item.text)
        if parsed:
            continue
        # TODO: REPLACE AFTER FIXING TEXMEX
        # most item is more robust than max item
        textsize = utila.flatten(
            [[item.size] * (item.end - item.start) for item in item.style])
        textsize = utila.mode(textsize)
        if textsize < 15.0:  # TODO: HOLY VALUE
            continue
        result.append(item.text.strip())
    if not result:
        return None
    if len(result) > 1:
        return None
    return result[0]
