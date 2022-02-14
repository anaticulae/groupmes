# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table of figures extractor
==========================
"""

import configo
import elements
import serializeraw
import utila

import groupme.feature.figuretable
import groupme.pageselector
import groupme.toc.run
import groupme.toc.strategy
import groupme.toc.toc.create

# minimal percentage of tabletable lines per page
TOFS_PER_PAGE_MIN = configo.HV_PERCENT_PLUS(default=20, limit=100)


def work(
    text: str,
    textpositions: str,
    headerfooter: str,
    sizeandborder: str,
    pages: tuple = None,
) -> str:
    """Extract table of figures out of `document`.

    Args:
        text(str): path to load document
        textpositions(str): path to load document textpositions
        headerfooter(str): path with header and footer to determine
                           content border.
        sizeandborder(str): path with page sizes and content border
        pages(tuple): tuple of selected pages
    Returns:
        dump of extracted table of content
    """
    navigators = serializeraw.create_pagetextcontentnavigators_fromfile(
        text,
        textpositions,
        sizeandborderpath=sizeandborder,
        headerfooterpath=headerfooter,
        pages=pages,
    )
    selected = groupme.pageselector.select_contentpages(
        navigators,
        wrong_table=NO_TABLES,
        valid_lines_perpage_min=TOFS_PER_PAGE_MIN,
    )
    # select toc pages only
    navigators = utila.select_pages(navigators, pages=selected)

    loaded = groupme.toc.strategy.ExtractionData(content=navigators)
    extracted = groupme.toc.run.extract(loaded)

    flat = utila.flatten(extracted.content)
    leveled = groupme.toc.toc.create.groupby_level(flat)

    dumped = serializeraw.dump_toc(leveled)
    return dumped


NO_TABLES = (elements.ABBREVIATION | elements.TOC | elements.FIGURETABLE |
             elements.SYMBOLTABLE)
