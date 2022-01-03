# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import re

import utila

import groupme.toc
import groupme.utils.text_regex


def parse(line: str) -> groupme.toc.TocLine:
    assert isinstance(line, str), type(line)
    # TODO: REMOVE LATER
    line = line.strip()
    for pattern in [
            EXTENDED_PATTERN_LETTER,
            EXTENDED_PATTERN,
            NO_DOTS,
            NO_LEVEL,
            DICTIONARY,
    ]:
        matched = re.match(pattern, line)
        if matched:
            return extract_match(matched)
    return None


LEVEL = r'(?P<level>(\d{1,2}\.)+\d{0,2})'
LEVEL_DOTTED_OPTIONAL = r'(?P<level>(\d{1,2}\.?)+\d{0,2})'

LEVEL_LETTER = r"""(?P<level>
                    (
                    (A|B|C|D)\.?|
                    (A|B|C|D)\.(\d{1,2}\.?)+\d{0,2}|
                    Anhang[ ](A|B|C|D)\: # TODO: Exclude Anhang and :
                    )
                )"""

TEXT = (
    '(?P<text>'
    fr'{groupme.utils.text_regex.UC_NWS}'  # ensure that text does not start with whitespace
    fr'{groupme.utils.text_regex.UC_WS_NL}+?'
    fr'{groupme.utils.text_regex.UC_NWS}+?'  # ensure that text does not end with whitespace
    ')')

WHITESPACES = r'[ ]{1,5}'
WHITESPACES_OPT = r'[ ]{0,3}'
DOTTED = r'([ \.…]+)'
# TODO: ENSURE TO NOT CUTTING CONTENT WHICH ENDS: "BASS.10 => BASS PAGE: 10"
PAGE = r"""
    \b(
        ((S|P)\.[ ]{0,3})?      # optional S. or P.
        (?P<page>
            (
                \d{1,3}|                # arabic
                [IiVvXx]{1,6}           # roman
            )
        )
    )\b
"""

EXTENDED_PATTERN = re.compile(
    ('^'
     f'{LEVEL_DOTTED_OPTIONAL}'
     f'{WHITESPACES}'
     f'{TEXT}'
     f'{DOTTED}'
     f'{PAGE}'
     '$'),
    re.VERBOSE | re.MULTILINE | re.UNICODE,
)

EXTENDED_PATTERN_LETTER = re.compile(
    ('^'
     f'{LEVEL_LETTER}'
     f'{WHITESPACES}'
     f'{TEXT}'
     f'{DOTTED}'
     f'{PAGE}'
     '$'),
    re.VERBOSE | re.MULTILINE | re.UNICODE,
)

NO_DOTS = re.compile(
    ('^'
     f'{LEVEL_DOTTED_OPTIONAL}'
     f'{WHITESPACES}'
     f'{TEXT}'
     f'{WHITESPACES}'
     f'{PAGE}'
     '$'),
    re.VERBOSE | re.MULTILINE | re.UNICODE,
)

NO_LEVEL = re.compile(
    ('^'
     f'{TEXT}'
     f'{WHITESPACES_OPT}'
     f'{DOTTED}'
     f'{WHITESPACES_OPT}'
     f'{PAGE}'
     '$'),
    re.VERBOSE | re.MULTILINE | re.UNICODE,
)

#  r'([ \.]{2,})'
LIST = [
    'A',
    'Abbildungsverzeichnis',
    'Anhang',
    'Bildquellen',
    'Glossar',
    'Internetquellen',
    'Listings',
    'Literatur',
    'Literaturverzeichnis',
    'Tabellenverzeichnis',
    r'Eidesstattliche\ Erklärung',
]

JOINED_LIST = '|'.join(LIST)

DICTIONARY = re.compile(
    ('^'
     f'(?P<text>({JOINED_LIST}))'
     r'([ \.]{0,})'
     f'{PAGE}'),
    re.VERBOSE | re.UNICODE,
)


def extract_match(match: re.Match) -> groupme.toc.TocLine:
    assert isinstance(match, re.Match), type(match)
    level, title, page = None, match['text'], None
    with contextlib.suppress(IndexError):
        page = match['page']
    with contextlib.suppress(IndexError):
        level = match['level']
    # prepare title
    title = title.replace('\n', ' ')
    title = utila.normalize_whitespaces(title)
    # create result
    result = groupme.toc.TocLine(
        level=level,
        title=title,
        page=page,
        raw=utila.extract_match(match),
    )
    return result
