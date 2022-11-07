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
    pagenumbers = []  # TODO: ENABLE LATER
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
        if pagenumber and pagenumber.footer:
            if not item.header and not item.footer:
                item.footer = pagenumber.footer
        result.content.append(item)
    return result


def load_pagenumbers(
    pagenumber,
    pages: tuple,
) -> iamraw.PageContentFooterHeaders:
    result = iamraw.PageContentFooterHeaders(content=[])
    result.__stategy__ = 'pagenumber'
    loaded = serializeraw.load_pagenumbers(pagenumber, pages=pages)
    single = utila.Single()
    for item in loaded:
        pdfpage = item.pdfpage  # pylint:disable=E1101
        # TODO: MAY REMOVE LATER
        if single.contains(pdfpage):
            utila.error(f'duplicated pagenumber/pdfpage: {item}')
            continue
        pageinfo = iamraw.PageInformation(value=item.detected)  # pylint:disable=E1101
        footer = iamraw.FixedFooterInfo(page=pageinfo)
        page = iamraw.PageContentFooterHeader(
            page=pdfpage,
            footer=footer,
        )
        result.content.append(page)
    return result
