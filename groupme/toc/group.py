# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import re

import configo
import elements
import iamraw
import utila

import groupme.toc

APPENDIX_LEVEL = configo.HV_INT_PLUS(default=100)


def groupby_chapter(items: groupme.toc.TocLines):
    """Group by chapter."""
    # TODO: DONT KNOW WHY WE NEED THIS?
    assert isinstance(items, list), type(items)
    for item in items:
        assert isinstance(item, groupme.toc.TocLine), type(item)
    result = []
    collected = []
    for item in items:
        if item.level is None:
            if collected:
                result.append(collected)
                collected = []
            result.append([item])
            continue
        if collected and collected[-1].level[0] != item.level[0]:
            result.append(collected)
            collected = [item]
        else:
            collected.append(item)
    if collected:
        result.append(collected)
    return result


@dataclasses.dataclass
class Level:
    # TODO: MOVE TO IAMRAW
    value: int = None
    raw: str = dataclasses.field(compare=False, default=None)

    def __int__(self):
        return self.value


class RomanLevel(Level):
    pass


class StepLevel(Level):
    pass


@dataclasses.dataclass
class AppendixLevel(Level):
    """\
    Example::
        A.1.1
    """
    character: str = None

    def __int__(self):
        return APPENDIX_LEVEL


def level(item: str) -> Level:
    """Determine level out of parsed level string.

    Examples:
      - IV Anhang
      - 4.1.1 Datenschicht
      - 5 Implementierung
      - None Literaturverzeichnis

    >>> level('A')
    AppendixLevel(value='A', raw='A', character='A')
    """
    # TODO: SUPPORT 1. Abbildung
    # TODO: SUPPORT 1. Abb.
    # In the current implementation there are valid cause of 'A' in Abb/
    # Abbildung, but this is not the correct Point.
    if item is None:
        return None

    number = elements.level_numbered(item)
    if number is not None:
        return Level(value=number, raw=item)

    if value := utila.arabic(item):
        return RomanLevel(value=value, raw=item)

    try:
        letter, _ = item.split('.', maxsplit=1)
        letter = letter.upper()
    except ValueError:
        # TODO: REMOVE THIS HACK AFTER FIXING LINEREGEX
        letter = item.replace('Anhang', '').replace(':', '').strip()

    if letter in ('A', 'B', 'C', 'D'):
        result = AppendixLevel(value=letter, character=letter, raw=item)
        return result

    if converted := level_steps(item):
        result = StepLevel(value=converted, raw=item)  # pylint:disable=R0204
        return result

    utila.error(f'could not convert to level: {item}')
    return None


# TODO: MOVE TO ELEMENTS
def groupby_level(toc: groupme.toc.TocLines) -> iamraw.Toc:
    if isnumbered(toc):
        return groupby_level_numbered(toc)
    return groupby_level_steps(toc)


def isnumbered(toc) -> bool:
    if not toc:
        return True
    levels = len([
        item for item in toc if item.level and
        elements.headline.level.level_numbered_dots(item.level)
    ])
    rate = levels / len(toc)
    if rate < 0.8:
        return False
    return True


def groupby_level_numbered(toc: groupme.toc.TocLines) -> iamraw.Toc:
    """Create `iamraw.Toc` out of list of `groupme.toc.TocLine

    Determine level of toc line and replace it with determined int-level.

    Args:
        toc: extracted table of content.
    Returns:
        Table of content with replaced levels.`
    """
    assert isinstance(toc, list), type(toc)
    outlines = []
    for line in toc:
        if not line:
            utila.error(f'problem while processing lines: {line}')
            continue
        if not isinstance(line, groupme.toc.TocLine):
            continue
        levels = determine_level(line.level)
        section = iamraw.SectionRaw(
            level=levels,
            page=line.page,
            title=line.title,
            raw=line.raw,
            raw_location=line.raw_location,
        )
        outlines.append(section)
    outlines = level_zero(outlines)
    result = iamraw.create_toc(outlines)
    return result


def level_zero(items):
    """Ensure that no toc has level zero

    Problem:
        1 Einleitung
        1.1 Aufbau der Arbeit
        update every level to ensure
    """
    # TODO: REMOVE THIS?
    level_min = min([item.level for item in items], default=utila.INF)
    if not level_min:
        for item in items:
            item.level = item.level + 1
    return items


def determine_level(levels) -> int:
    if levels is None:
        return 1
    numbered = elements.level_numbered(levels)
    if numbered is None:
        return 1
    return numbered


def groupby_level_steps(toc: groupme.toc.TocLines) -> iamraw.Toc:
    """\
    Example
        A Lateinische Buchstaben
            I. Roman numbers
                1. Arabische Zahlen
                    a. Lateinische Kleinbuchstaben
    """
    assert isinstance(toc, list), type(toc)
    outlines = []
    for line in toc:
        if not line:
            utila.error(f'problem while processing lines: {line}')
            continue
        if not isinstance(line, groupme.toc.TocLine):
            continue
        levels = level_steps(line.level)
        section = iamraw.SectionRaw(
            level=levels,
            page=line.page,
            title=line.title,
            raw=line.raw,
            raw_location=line.raw_location,
        )
        outlines.append(section)
    outlines = level_zero(outlines)
    result = iamraw.create_toc(outlines)
    return result


def level_steps(raw: str) -> int:  # pylint:disable=R0911
    """Convert number to raw level.

    Example:
        A Lateinische Buchstaben
            I. Roman numbers
                1. Arabische Zahlen
                    a. Lateinische Kleinbuchstaben

    >>> level_steps('KAPITEL 1 WAS IST HUMAN SECURITY?')
    1
    >>> level_steps('A. Was ist Sicherheit?')
    2
    >>> level_steps('III. Umwelt und Klimawandel')
    3
    >>> level_steps('2. Politische und wenige(r) rechtliche Aspekte')
    4
    >>> level_steps('a) Konzepte')
    5
    >>> level_steps('dd) Bewertung')
    6
    """
    # TODO: MOVE TO ELEMENTS
    raw = raw.strip() if raw else None
    if not raw:
        return 1
    if re.match(r'^(KAPITEL)[ ]{1,3}\d{1,2}', raw, re.IGNORECASE):
        return 1
    if re.match(r'^(A|B|C|D|E|F|G|H)\.', raw, re.IGNORECASE):
        return 2
    if re.match(r'^(I|II|III|IIII|IV|V|VI|VII|VIII)\.?', raw, re.IGNORECASE):
        return 3
    if re.match(r'^\d{1,2}\.', raw, re.IGNORECASE):
        return 4
    if re.match(r'^[a-h]\)', raw, re.IGNORECASE):
        return 5
    if re.match(r'^[a-h]{2}\)', raw, re.IGNORECASE):
        return 6
    assert 0, raw
    return None
