# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila

import groupme.footnotes.utils


def parse(
    content: list,
    width: float = 594.0,
    pagenumber: int = None,
) -> list:
    """\
    Args:
        content(list): content of footnote area
        width(float): width in pixel of current page. As default use DINA4.
        pagenumber(int): pdf raw page number
    Returns:
        List of parsed footnotes
    """
    grouped = groupme.footnotes.utils.group_footnote_area(content)
    result = []
    for number, note in grouped:
        x0 = number.bounding[0]
        # TODO: REPLACE WITH DUE PAGE SIZE FORMATS
        if x0 >= groupme.footnotes.utils.MAX_FOOTNOTE_X0(width):
            # potential highnote is located too right
            continue
        try:
            notenumber = int(number.text)
        except ValueError:
            utila.error(f'could not convert to int: {number.text}')
            notenumber = number.text
        if not note.text.strip():
            utila.error(f'could not parse footnote: {number}, no text content')
            continue
        bounding = tuple(number.bounding)
        text = utila.normalize_text(note.text)
        footnote = iamraw.FootRawNote(
            bounding=bounding,
            number=notenumber,
            raw='',  # TODO: REMOVE THIS?
            style=(number.style, note.style),
            text=text,
            page=pagenumber if pagenumber is not None else -1,
        )
        result.append(footnote)
    return result
