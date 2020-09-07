# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table of content extractor
==========================

Outdated approaches
-------------------

- collect title and check if sequence exists again in the document

"""

import configo
import serializeraw
import utila

import groupme.feature
import groupme.feature.figuretable
import groupme.toc
import groupme.toc.extractor
import groupme.toc.group
import groupme.toc.strategy

# minimal percentage of toc lines per page
MIN_TOCS_PER_PAGE = configo.HV_PERCENT_PLUS(0.2, limit=1.0).value

# limit possible toc to the first 15 pages
POSSIBLE_PAGES = utila.make_tuple(15)


def work(
        text: str,
        textpositions: str,
        headerfooter: str,
        sizeandborder: str,
        pages: tuple = None,
) -> str:
    """Extract table of content out of `document`.

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
    # select toc pages only
    selected = groupme.pageselector.select_contentpages(
        textnavigators=utila.select_pages(navigators, POSSIBLE_PAGES),
        wrong_table=NO_TOC,
        skip_higherqual_level_three=False,
        min_valid_lines_perpage=MIN_TOCS_PER_PAGE,
    )
    navigators = utila.select_pages(navigators, pages=selected)

    loaded = groupme.toc.strategy.load(navigators)
    extracted = groupme.toc.extractor.extract(loaded)

    flat = utila.flatten(extracted.content)
    leveled = groupme.toc.group.groupby_level(flat)

    dumped = serializeraw.dump_toc(leveled)
    return dumped


NO_TOC = {
    'Abbildungsverzeichnis',
    'Abkürzungsverzeichnis',
    'Anhang',
    'Eidesstattliche Erklärung',
    'Glossar',
    'Literaturverzeichnis',
    'Tabellenverzeichnis',
}
