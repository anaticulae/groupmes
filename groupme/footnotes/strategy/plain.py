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
    collected = prepare(content)
    result = []
    # parse footnote
    for multiline in collected:
        parsed = parse_group(multiline, width=width, pagenumber=pagenumber)
        if not parsed:
            continue
        result.append(parsed)
    return result


def parse_group(
    multiline: list,
    width: float,
    pagenumber: int,
) -> iamraw.FootNoteRaw:
    x0 = multiline[0].bounding[0]  # first line x0
    if x0 >= groupme.footnotes.layout.FOOTNOTE_X0_MAX(width):
        # potential highnote is located too right
        return None
    raw = utila.NEWLINE.join([item.text.strip() for item in multiline])
    raw = groupme.footnotes.utils.hyperlink_improve(raw)
    number, content = groupme.footnotes.utils.search_footnote(raw)
    bounding = tuple(multiline[0].bounding)
    text = utila.normalize_text(
        content,
        normalize_spaces=True,
        strips=True,
    )
    footnote = iamraw.FootNoteRaw(
        bounding=bounding,
        number=number,
        style=None,
        page=pagenumber if pagenumber is not None else -1,
        text=text,
        raw=raw,
        raw_number='' if number == -1 else str(number),
    )
    return footnote


def prepare(content: list) -> list:
    neighbors = groupme.footnotes.layout.connect_neighbors(content)
    collected = utila.flatten([merges(neighbor) for neighbor in neighbors])
    return collected


MERGE_LINE_MIN = configo.HV_INT_PLUS(default=len('1. Ebd.'))


def merges(content, merge_line_min: int = MERGE_LINE_MIN):
    if not content:
        return []
    collected = [[content[0]]]
    # merge multiple lines
    for line in content[1:]:
        if new_footnote(line.text, merge_line_min):
            collected.append([line])
        else:
            collected[-1].append(line)
    return collected


def new_footnote(text, merge_line_min: int) -> bool:
    text = text.strip()
    matched = groupme.footnotes.utils.NUMBER_TEXT.match(text)
    if not matched:
        return False
    if len(text) < merge_line_min:
        return False
    return True
