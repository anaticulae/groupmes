# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import iamraw
import utila

import groupme.footnotes

NUMBER_TEXT = r'(?P<number>\d+)[ ]*(?P<text>.{3,})'


def parse(content: list, width: float = 594.0, pagenumber: int = None) -> list:
    neighbors = groupme.footnotes.neighbors(content)
    collected = utila.flatten([merges(neighbor) for neighbor in neighbors])
    result = []
    # parse footnote
    for multiline in collected:
        x0 = multiline[0].bounding[0]  # first line x0
        if x0 >= groupme.footnotes.MAX_FOOTNOTE_X0(width):
            # potential highnote is located too right
            continue
        text = ''.join([item.text for item in multiline])
        matched = re.match(NUMBER_TEXT, text, flags=re.MULTILINE | re.DOTALL)
        if not matched:
            number, content = -1, text
        else:
            number, content = int(matched['number']), matched['text']
        bounding = tuple(multiline[0].bounding)
        text = utila.normalize_text(content.strip())
        footnote = iamraw.FootRawNote(
            bounding=bounding,
            number=number,
            style=None,
            page=pagenumber if pagenumber is not None else -1,
            text=text,
        )
        result.append(footnote)
    return result


def merges(content):
    if not content:
        return []
    collected = [[content[0]]]
    # merge multiple lines
    for line in content[1:]:
        text = line.text.strip()
        matched = re.match(NUMBER_TEXT, text, re.MULTILINE)
        if not matched:
            collected[-1].append(line)
        else:
            collected.append([line])
    return collected
