# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table of figures extractor
==========================
"""

import configo
import geostrat
import iamraw
import serializeraw
import utila

import groupme.pageselector
import groupme.toc
import groupme.toc.extractor
import groupme.toc.group
import groupme.toc.strategy

# minimal percentage of figure lines per page
MIN_TOFS_PER_PAGE = configo.HV_PERCENT_PLUS(20, limit=100.0).value


def work(
        text: str,
        textpositions: str,
        oneline_text: str,
        oneline_textpositions: str,
        headerfooter: str,
        sizeandborder: str,
        pages: tuple = None,
) -> str:
    """Extract table of figures out of `document`.

    Args:
        text(str): path to load document
        textpositions(str): path to load document textpositions
        oneline_text(str): oneline document
        oneline_textpositions(str): oneline document positions
        headerfooter(str): path with header and footer to determine
                           content border.
        sizeandborder(str): path with page sizes and content border
        pages(tuple): tuple of selected pages
    Returns:
        dump of extracted table of content
    """
    oneline = serializeraw.create_pagetextcontentnavigators_fromfile(
        oneline_text,
        oneline_textpositions,
        sizeandborderpath=sizeandborder,
        headerfooterpath=headerfooter,
        pages=pages,
    )
    result = oneline_figure_strategy(oneline)
    if not result:
        ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
            text,
            textpositions,
            sizeandborderpath=sizeandborder,
            headerfooterpath=headerfooter,
            pages=pages,
        )
        result = doublecolumn_figure_strategy(ptcns)
    result = groupme.toc.group.groupby_level(result)  # pylint:disable=R0204
    dumped = serializeraw.dump_toc(result)
    return dumped


def oneline_figure_strategy(oneline) -> iamraw.Toc:
    selected = groupme.pageselector.select_contentpages(
        oneline,
        wrong_table=NO_FIGURES,
        min_valid_lines_perpage=MIN_TOFS_PER_PAGE,
    )
    # select toc pages only
    oneline = utila.select_pages(oneline, pages=selected)

    loaded = groupme.toc.strategy.load(oneline)
    extracted = groupme.toc.extractor.extract(loaded)

    flat = utila.flatten(extracted.content)
    return flat


def doublecolumn_figure_strategy(ptcns) -> iamraw.Toc:
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
        wrong_table=NO_FIGURES,
        min_valid_lines_perpage=MIN_TOFS_PER_PAGE,
    )
    if not pages:
        return []

    ptcns = utila.select_pages(ptcns, pages)
    extracted = [parse(item) for item in ptcns]

    result = utila.flatten(extracted)
    return result


NO_FIGURES = {
    'Abkürzungsverzeichnis',
    'Glossar',
    'Inhalt',
    'Inhaltsverzeichnis',
    'Literaturverzeichnis',
    'Tabellenverzeichnis',
}
