# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import german
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
        text = line.text.strip()
        matched = groupme.footnotes.utils.NUMBER_TEXT.match(text)
        if matched and len(text) >= merge_line_min:
            collected.append([line])
        else:
            collected[-1].append(line)
    return collected


def hyperlink_improve(text: str) -> str:
    r"""\
    >>> hyperlink_improve('found at https://aur.\narchlinux.org/trusted-user/TUbylaws.html. There')
    'found at https://aur.archlinux.org/trusted-user/TUbylaws.html. There'

    Do not fail on empty line.
    >>> hyperlink_improve('htpp://www.google.de\n\nhello.')
    'htpp://www.google.de  hello.'
    """
    # TODO: MOVE TO GERMAN?
    splitted = text.splitlines()
    if len(splitted) == 1:
        # no merging required
        return text
    result = splitted[0]
    for item in splitted[1:]:
        lastitem = result.split()[-1]
        if not german.links(lastitem):
            result += ' ' + item
            continue
        firstitem = item.split()
        if not firstitem:
            # newline
            result += ' '
            continue
        # select first word
        firstitem = firstitem[0]
        # skip last char to avoid single word with sentence sign
        firstitem = firstitem[0:-1]
        if any(char in firstitem for char in '/-.:'):
            # merge link
            result += item
            continue
        # no link to merge
        result += ' ' + item
    return result
