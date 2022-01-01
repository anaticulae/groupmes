# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import utila


def work(
    text: str,
    textpositions: str,
    sizeandborder: str,
    headerfooter: str,
    pages: tuple = None,
) -> str:
    """Extract table of content out of `document`.

    Args:
        text(str): path to load document
        textpositions(str): path to load document textpositions
        sizeandborder(str): path with page sizes and content border
        headerfooter(str): path with header and footer to determine
                           content border.
        pages(tuple): tuple of selected pages
    Returns:
        dump of extracted content bounding boxes
    """
    navigators = serializeraw.create_pagetextcontentnavigators_fromfile(
        text,
        textpositions,
        sizeandborderpath=sizeandborder,
        headerfooterpath=headerfooter,
        pages=pages,
    )
    result = []
    for page in navigators:
        top, bottom = page.content.top, page.content.bottom
        top, bottom = utila.roundme((top, bottom))
        result.append(
            iamraw.ContentBoundingBox(
                page=page.page,
                top=top,
                bottom=bottom,
            ))
    dumped = serializeraw.dump_contentboundingbox(result)
    return dumped
