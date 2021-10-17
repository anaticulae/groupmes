# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import math
import typing

import configo
import iamraw
import texmex
import utila

VERTICAL_LINE_DIFF_OF_HIGHNOTES = configo.HV_FLOAT_PLUS(default=15.0)
HIGHNOTE_RISE_MIN = configo.HV_FLOAT_PLUS(default=3.0)

FOOTNOTE_X0_MAX = configo.HolyTable(
    items=(
        (440, 100),  # TODO: US Letter?
        (550, 150),  # DINA4
    ),
    left_outranges_none=False,
    right_outranges_none=False,
)


def group_footnote_area(content):
    neighbors_ = neighbors(content)
    result = []
    for group in neighbors_:
        splitted = split_textinfo(group)
        merged = merge_online(splitted)
        result.extend(merged)
    return result


def neighbors(items):
    if not items:
        return []
    result = [[items[0]]]
    for item in items[1:]:
        before = result[-1][-1]
        if connected(before, item):
            result[-1].append(item)
        else:
            result.append([item])
    return result


def split_textinfo(content) -> list:
    """Split text by `hightnote` and preserve TextInfo.

    Returns:
        list of a tuple of highnote and content
    """
    assert isinstance(content, list), type(content)
    result = []
    highnote = None
    collected = []
    for item in content:
        for style in item.style.content:
            if style.rise >= HIGHNOTE_RISE_MIN:
                if highnote:
                    result.append((highnote, union(collected)))
                    collected = []
                style = style.copy()
                highnote = texmex.TextInfo(
                    text=item.text[style.start:style.end],
                    style=style,
                    bounding=char_bounding(item.bounding, item.text, style),
                )
                style.start = 0
                style.end = len(highnote.text)
            else:
                bounding = iamraw.split_x(
                    item.bounding,
                    style.start,
                    len(item.text),
                )
                collected.append(TextChunk(item.text, style, bounding))
    if highnote:
        # ?THERE IS ALWAYS A REST?
        result.append((highnote, union(collected)))
    return result


def merge_online(items) -> list:
    """Ensure that high notes are located on a vertical line. Therefore
    we have to ignore highnotes which are located inside the text and
    not part of the text flow.

    Steps:
        1. Determine the most left highnotes
        2. Adjust highnotes on most left one
        3. Merge other highnotes into text
    """
    if not items:
        return []
    result = []
    mostleft = min([item.bounding.x0 for item, _ in items])
    high, collected = None, []
    for highnote, content in items:
        diff = math.fabs(highnote.bounding.x0 - mostleft)
        if diff > VERTICAL_LINE_DIFF_OF_HIGHNOTES:
            # highnote in content
            collected.append(shrink_tostyle(highnote.text, highnote.style))
            collected.extend([
                shrink_tostyle(content.text, style) for style in content.style
            ])
        else:
            # new highnotes
            if high:
                result.append((high, union(collected)))
            high = highnote
            collected = [
                shrink_tostyle(content.text, style) for style in content.style
            ]
    result.append((high, union(collected)))
    return result


LEFTRIGHT_DIFF_MAX = configo.HV_FLOAT_PLUS(default=20.0)

SAMEORIGIN_DIFF_MAX = configo.HV_FLOAT_PLUS(default=35.0)

SAMELINE_DIFF_MAX = configo.HV_FLOAT_PLUS(default=5.0)

UNDERFIRST_DIFF_MAX = configo.HV_FLOAT_PLUS(default=10.0)


def connected(first, second):
    leftright = utila.near(
        first.bounding.x1,
        second.bounding.x0,
        diff=LEFTRIGHT_DIFF_MAX,
    )
    # plus indention
    sameorigin = utila.near(
        first.bounding.x0,
        second.bounding.x0,
        diff=SAMEORIGIN_DIFF_MAX,
    )
    sameline = utila.near(
        first.bounding.y0,
        second.bounding.y0,
        diff=SAMELINE_DIFF_MAX,
    )
    underfirst = utila.near(
        first.bounding.y1,
        second.bounding.y0,
        diff=UNDERFIRST_DIFF_MAX,
    )
    result = (leftright or sameorigin) and (sameline or underfirst)
    return result


@dataclasses.dataclass
class TextChunk:
    text: str = None
    style: texmex.TextStyle = None
    bounding: iamraw.BoundingBox = None


TextChunks = typing.List[TextChunk]


def shrink_tostyle(text: str, style) -> TextChunk:
    text = text[style.start:style.end]
    style = style.copy()
    style.start, style.end = 0, len(text)
    return TextChunk(text, style, None)


def union(chunks: TextChunks) -> texmex.TextInfo:
    raw = ''
    content = []
    for chunk in chunks:  # pylint:disable=W0612
        start = len(raw)
        raw += chunk.text[chunk.style.start:chunk.style.end]
        end = len(raw)
        section_style = chunk.style.copy()
        section_style.start, section_style.end = start, end
        content.append(section_style)
    result = texmex.TextInfo(
        text=raw,
        style=texmex.TextStyle(content=content),
    )
    return result


def char_bounding(
    bounding: iamraw.BoundingBox,
    text: str,
    style: texmex.TextStyle,
) -> iamraw.BoundingBox:
    width = bounding.x1 - bounding.x0
    char_width = width / len(text)
    x0 = bounding.x0 + char_width * style.start
    x1 = bounding.x0 + char_width * style.end
    result = iamraw.BoundingBox(x0, bounding.y0, x1, bounding.y1)
    return result
