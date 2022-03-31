# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import configo
import utila

HIGHNOTE_RISE_MIN = configo.HV_FLOAT_PLUS(default=3.0)

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


NUMBER_TEXT = utila.compiles(
    r"""
    \[?
    (?P<number>\d{1,4})
    \]?
    (?!
        (   # do not detect 229ff. as footnote
            \d{0,4}(f|p){1,2}\.
        )
        |
        (   # do not detect 2.1.3 as footnote
            \.\d{1,2}\.
        )
    )
    [ ]{0,4}
    (?P<text>.{3,})
""",
    flags=(re.X | re.MULTILINE | re.DOTALL),
)


def search_footnote(text):
    r"""\
    >>> search_footnote('61 UNDP HDR 2007/2008, S.\n229ff. Die Weltfinanzkrise 2008-9'
    ... '\n62 In der Tat wurde der Begriff bereits')
    (61, 'UNDP HDR 2007/2008, S.\n229ff. Die Weltfinanzkrise 2008-9\n62 In der Tat wurde der Begriff bereits')
    >>> search_footnote('229ff. Die Weltfinanzkrise 2008-9')
    (-1, '229ff. Die Weltfinanzkrise 2008-9')
    """
    matched = NUMBER_TEXT.match(text)
    if not matched:
        number, content = -1, text
    else:
        number, content = int(matched['number']), matched['text']
    return number, content


def ishighnote(style, text: str) -> bool:
    highnote_occurs = style.rise >= HIGHNOTE_RISE_MIN
    if not highnote_occurs:
        return False
    text = text[style.start:style.end].strip()
    if NUMBER.match(text):
        return True
    return False
