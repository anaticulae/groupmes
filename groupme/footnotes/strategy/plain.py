# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import utila

import groupme.footnotes.layout
import groupme.footnotes.utils


def parse(content: list, width: float = 594.0, pagenumber: int = None) -> list:
    neighbors = groupme.footnotes.layout.neighbors(content)
    collected = utila.flatten([merges(neighbor) for neighbor in neighbors])
    result = []
    # parse footnote
    for multiline in collected:
        x0 = multiline[0].bounding[0]  # first line x0
        if x0 >= groupme.footnotes.layout.FOOTNOTE_X0_MAX(width):
            # potential highnote is located too right
            continue
        text = ''.join([item.text for item in multiline])
        number, content = groupme.footnotes.utils.search_footnote(text)
        bounding = tuple(multiline[0].bounding)
        text = utila.normalize_text(content, normalize_spaces=True, strips=True)
        footnote = iamraw.FootRawNote(
            bounding=bounding,
            number=number,
            style=None,
            page=pagenumber if pagenumber is not None else -1,
            text=text,
            raw=content,
            raw_number='' if number == -1 else str(number),
        )
        result.append(footnote)
    return result


MERGE_LINE_MIN = configo.HV_INT_PLUS(default=len('1. Ebd.'))


def merges(content, merge_line_min: int = MERGE_LINE_MIN):
    if not content:
        return []
    collected = [[content[0]]]
    # merge multiple lines
    for line in content[1:]:
        text = line.text.strip()
        matched = groupme.footnotes.utils.NUMBER_TEXT.match(text)
        if matched and len(text) >= merge_line_min:
            collected.append([line])
        else:
            collected[-1].append(line)
    return collected
