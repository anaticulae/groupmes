# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""toc - regex extractor
=====================

Extract headlines based on regex pattern.

design decision
---------------

Should we support following whitespaces?

    It is not required to support lines with ending whitespaces. Following
    whitespace puts water into the wine and leads to more missmatchings. The
    better approach is to improve the pdf-parser to avoid following
    whitespaces.

    See: :class:`tests.groupme_.toc.test_regex.test_extract_toc_line_whitespace_decission`.
"""

import copy
import math
import re

import configo
import iamraw
import utila

import groupme.toc
import groupme.toc.basic.lineregex
import groupme.toc.strategy

TOC_LINE_LENGTH_MAX = configo.HV_FLOAT_PLUS(default=250.0)

ONELINE_MERGE_Y_DIFF_MAX = configo.HV_FLOAT_PLUS(default=5.0)


class RegexTocExtractor(groupme.toc.strategy.ExtractorStrategy):

    def result(self) -> groupme.toc.strategy.ExtractionResult:
        parsed = [parse_page(page) for page in self.loaded.content]
        flat = utila.flatten(parsed)
        grouped = groupme.toc.strategy.group(flat)
        return grouped


def parse(content: str) -> groupme.toc.TocLines:
    """Parse table of content via regex.

    Args
        content(str): content of block of text
    Returns:
        ordered list form top to down of parse table of content
    Pattern:

        with level:

        .. code-block :: none

            X.      Chapter ........... 1
            X.X     Section . . . . . . 3

        or no level:

        .. code-block :: none

            Eidesstattliche Erklärung ........... 69

    Regression test that this example last very long.
    >>> parse('35689101315161819202325262829303132331247111214172122242')
    []
    """
    duplicated = content
    result = []
    for pattern in [
            groupme.toc.basic.lineregex.EXTENDED_PATTERN,
            groupme.toc.basic.lineregex.EXTENDED_PATTERN_LETTER,
            groupme.toc.basic.lineregex.DICTIONARY,
            groupme.toc.basic.lineregex.NO_LEVEL,
            groupme.toc.basic.lineregex.NO_DOTS,
    ]:
        for line in re.finditer(pattern, content):
            item = groupme.toc.basic.lineregex.extract_match(line)
            if len(item.raw) <= 8:
                # TODO: REMOVE HACK LATER
                continue
            result.append(item)
            # remove already matched content to do not confuse lower
            # strict pattern
            content = content.replace(item.raw, '')
    # TODO: improve this
    for line in [item for item in content.splitlines() if item.strip()]:
        if re.match(r'^\d', line):
            continue
        matched = re.match(groupme.toc.basic.lineregex.NO_LEVEL, line)
        if not matched:
            continue
        matched = groupme.toc.basic.lineregex.extract_match(matched)
        result.append(matched)
    # remove duplications, which can occur when table of content is on the
    # same page as first headline.
    result = groupme.toc.remove_duplication(result)
    # remove long lines which can not be real lines
    result = [item for item in result if len(item.title) < TOC_LINE_LENGTH_MAX]
    # Ensure that toc list is ordered by position on pdf page
    result = groupme.toc.sort_byposition(result, duplicated)
    return result


def parse_page(page: iamraw.Page) -> groupme.toc.TocLines:
    """Merge `page` to raw string and extract the lines of table of content.

    Hint:
        see `parse`
    """
    # prepare data
    oneline_text = oneline(page)
    # remove single word line
    # HOMEWORK PAGE 4, remove `Inhaltsverzeichnis` in header.
    # # TODO: Look for a better header exclusion strategy
    # TODO: ONLY REQUIRED IF TO FEW PAGES ARE AVAILABLE, CAUSE HEADER
    # FOOTER STRATEGY NEEDS SOME DATA
    # TODO: THINK ABOUT REMOVING THIS
    result = [
        item for item in oneline_text.splitlines()
        if len(item.strip().split()) > 1
    ]
    result = utila.NEWLINE.join(result)
    result = parse(result)
    # setup parse page location
    for item in result:
        item.raw_location = page.page
    return result


def oneline(page) -> str:
    if isinstance(page, iamraw.Page):
        lines = utila.flatten([
            container for container in page
            if isinstance(container, iamraw.TextContainer)
        ])
        # lines = oneline_merge(lines)
        # TODO: CHECK FOR ONELINE_MERGE
        lines = [item.text for item in lines]
    else:
        # PageTextNavigator
        lines = oneline_merge(list(page))
        lines = [item.text for item in lines]
    lines = split_newlines(lines)
    lines = [item.strip() for item in lines]
    text = utila.NEWLINE.join(lines)
    return text


def oneline_merge(lines):
    """Merge layout if required."""
    # TODO: EXPERIMENTAL: IMPROVE, MOVE TO RAWMAKER?
    if not lines:
        return []
    # TODO: REPLACE BY .copy
    lines = [copy.deepcopy(item) for item in lines]
    # left to right
    lines = sorted(lines, key=lambda item: item.bounding.x0)
    # top to down
    lines = sorted(lines, key=lambda item: item.bounding.y0)
    result = [lines[0]]
    for item in lines[1:]:
        last_y = result[-1].bounding.y0
        current_y = item.bounding.y0
        if math.fabs(last_y - current_y) > ONELINE_MERGE_Y_DIFF_MAX:
            result.append(item)
            continue
        # TODO: MERGE BOUNDING
        # merge
        # do NOT strip second item, we do not want to lose the newline
        result[-1].text = result[-1].text.strip() + ' ' + item.text
    return result


def split_newlines(items):
    result = []
    for item in items:
        result.extend(item.splitlines())
    return result
