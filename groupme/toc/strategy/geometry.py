# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""table of content - geometry strategy
====================================
"""

import functools

import configo
import texmex
import utila

import groupme.toc.basic.group
import groupme.toc.strategy

HEADLINE_LEVEL_MAX = configo.HV_INT_PLUS(default=3)


class GeometryTocExtractor(groupme.toc.strategy.ExtractorStrategy):

    def result(self) -> groupme.toc.strategy.ExtractionResult:
        extracted = []
        for page in self.loaded.content:
            analyzed = analyse_page(page, self.textfeed)
            extracted.extend(analyzed)

        grouped = group_areas(extracted)
        content = [
            groupme.toc.basic.group.parse_group(group, page)
            for page, group in grouped
        ]
        # remove empty
        content = [item for item in content if item]
        content = utila.flatten(content)

        valid_content = groupme.toc.strategy.remove_nonconnected_tocs(content)
        invalid_content = [
            item for item in content if item not in valid_content
        ]

        valid_content = groupme.toc.strategy.group(valid_content)  # pylint:disable=R0204

        result = groupme.toc.strategy.ExtractionResult(
            content=valid_content.content,
            invalid=invalid_content,
        )
        assert isinstance(result.content, list), type(result.content)
        return result

    @functools.cached_property
    def textfeed(self):
        feeds = texmex.document_textfeed(
            self.loaded.content,
            count=HEADLINE_LEVEL_MAX.value,
        )
        feed = sorted(feeds)
        return feed


def analyse_page(
    navigator: texmex.PageTextContentNavigators,
    level_feed: list,
) -> list:
    contentborder = navigator.content
    navigator: 'PTN' = groupme.toc.strategy.remove_headline(navigator)
    textbounds = texmex.textbounds(navigator, contentborder)
    result = []
    for item in textbounds:
        # document_text feed is computed from left page border to text.
        # text feed is computed from expected content start till text start
        # convert local to global text feed
        xdist = contentborder.left + item.bounds.leftdist
        current_level = level(xdist, level_feed)
        result.append((navigator.page, (current_level, item)))
    return result


def group_areas(items):
    result = []
    current = []
    lastpage = -1
    for page, (level_, item) in items:
        if current:
            if page >= (lastpage + 1):
                # one page space between toc groups, the toc can not be
                # connected.
                result.append((lastpage, current))
                current = []
            elif level_ == 0:  # pylint:disable=C2001
                # new group
                result.append((page, current))
                current = []
            # continue
        current.append(item)
        lastpage = page
    if current:
        result.append((lastpage, current))
    return result


def level(xdist, levels):
    for index, item in enumerate(levels):
        if xdist <= item:
            return index
    return None
