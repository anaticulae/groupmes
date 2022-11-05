# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import utila


def work(
    headnote: str,
    footnote: str,
    pagenumber: str,
    pages: tuple = None,
) -> str:
    headnote = serializeraw.load_headerfooter(headnote, pages=pages)
    footnote = serializeraw.load_headerfooter(footnote, pages=pages)
    pagenumber = load_pagenumbers(pagenumber, pages)
    merged = merge(headnote, footnote, pagenumber)
    dumped = serializeraw.dump_headerfooter(merged)
    return dumped


def merge(headnotes, footnotes, pagenumbers) -> list:
    result = iamraw.PageContentFooterHeaders(content=[])
    result.__strategy__ = 'hefopa'
    for page, (headnote, footnote, pagenumber) in utila.sync_pages(
        (headnotes, footnotes, pagenumbers)):
        if not any((headnote, footnote, pagenumber)):
            continue
        item = iamraw.PageContentFooterHeader(page=page)
        if footnote and footnote.footer:
            item.footer = footnote.footer
        if headnote:
            if headnote.header:
                item.header = headnote.header
            if headnote.footer:
                if not item.footer:
                    item.footer = headnote.footer
        result.content.append(item)
    return result


def load_pagenumbers(
    pagenumber,
    pages: tuple,
) -> iamraw.PageContentFooterHeaders:
    result = iamraw.PageContentFooterHeaders(content=[])
    result.__stategy__ = 'pagenumber'
    loaded = serializeraw.load_pagenumbers(pagenumber, pages=pages)
    for item in loaded:
        # PageNumber(pdfpage=4,
        header = iamraw.PageContentFooterHeader(page=item.pdfpage, header=item)  # pylint:disable=E1101
        result.content.append(header)
    return result
