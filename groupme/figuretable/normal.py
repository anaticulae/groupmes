# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import elements
import utila

import groupme.figuretable
import groupme.pageselector
import groupme.toc.run
import groupme.toc.strategy


def run(oneline) -> list:
    selected = groupme.pageselector.select_contentpages(
        oneline,
        wrong_table=groupme.figuretable.NO_FIGURES,
        valid_lines_perpage_min=groupme.figuretable.TOFS_PER_PAGE_MIN,
    )
    # select figure pages only
    oneline = utila.select_pages(oneline, pages=selected)
    oneline = [
        groupme.toc.strategy.remove_headline(
            page,
            headlines=elements.FIGURETABLE,
        ) for page in oneline
    ]
    loaded = groupme.toc.strategy.ExtractionData(content=oneline)
    extracted = groupme.toc.run.extract(loaded)

    flat = utila.flatten(extracted.content)

    flat = remove_figure_sequence(flat)
    return flat


FIGURE_REMOVE = utila.compiles(r"""
    ^
    (
        ABBILDUNG|
        ABB\.?|
        FIGURE|
        FIG.?
    )
    [ ]{0,2}
    \d{1,3}
    \:
    [ ]{0,2}
""")


def remove_figure_sequence(items) -> list:
    """Remove starting sequence which is a result of using toc-table
    parser."""
    for item in items:
        item.title = FIGURE_REMOVE.sub('', item.title)
    return items
