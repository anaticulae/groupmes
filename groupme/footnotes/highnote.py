# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import utila

import groupme.footnotes.utils

FOOTNOTE_TEXT_LENGTH_MIN = configo.HV_INT_PLUS(default=len('ebd.'))


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
        hashighnote = number is not None
        if hashighnote:
            x0 = number.bounding[0]
            # TODO: REPLACE WITH DUE PAGE SIZE FORMATS
            if x0 >= groupme.footnotes.utils.FOOTNOTE_X0_MAX(width):
                # potential highnote is located too right
                continue
        if len(note.text) < FOOTNOTE_TEXT_LENGTH_MIN:
            utila.debug(f'footnote too short: {note.text}')
            continue
        notenumber = parse_footnote_number(number.text) if hashighnote else None
        if not note.text.strip():
            utila.error(f'could not parse footnote: {number}, no text content')
            continue
        bounding = tuple(number.bounding) if hashighnote else None
        # TODO: USE STRIP=True AFTER UPGRADING UTILA
        text = utila.normalize_text(note.text).strip()
        footnote = iamraw.FootRawNote(
            bounding=bounding,
            number=notenumber,
            raw='',  # TODO: REMOVE THIS?
            raw_number=number.text.strip() if hashighnote else None,
            style=(number.style if hashighnote else None, note.style),
            text=text,
            page=pagenumber if pagenumber is not None else -1,
        )
        result.append(footnote)
    return result


NUMBER = utila.compiles(r'\[?(\d{1,4})\]?')


def parse_footnote_number(text: str) -> int:
    """\
    >>> parse_footnote_number('[133]')
    133
    """
    matched = NUMBER.match(text)
    if not matched:
        utila.error(f'could not convert to int: {text}')
        return text
    result = int(matched[1])
    return result
