# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import geostrat
import iamraw
import utila

import groupme.figuretable
import groupme.pageselector
import groupme.toc


def run(ptcns) -> iamraw.Toc:
    """\
    Abb. 1      SAM Skala in der 9-Punkte-Likert-Form
    Abb. 2      Mittelwerte der N ormierungen v on Lang et a l. ( 2005) und
                Libkuman et al. (2007)
    """

    def check_level(item: str):
        if 'Abb.' in item:
            return True
        if 'Abbildung' in item:
            return True
        return False

    def parse(ptcn) -> groupme.toc.TocLines:
        parsed = geostrat.dc_parse_page(ptcn)
        if not parsed:
            return []
        result = []
        for level, title in parsed:
            if not check_level(level):
                utila.debug(f'invalid figure level: {level}')
                continue
            item = groupme.toc.TocLine(
                level=level,
                title=title,
                raw_location=ptcn.page,
            )
            result.append(item)
        return result

    pages = groupme.pageselector.select_contentpages(
        ptcns,
        strategy=parse,
        wrong_table=groupme.figuretable.NO_FIGURES,
        valid_lines_perpage_min=groupme.figuretable.TOFS_PER_PAGE_MIN,
    )
    if not pages:
        return []

    ptcns = utila.select_pages(ptcns, pages)
    extracted = [parse(item) for item in ptcns]

    result = utila.flatten(extracted)
    return result
