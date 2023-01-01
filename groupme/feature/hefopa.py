# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import texmex
import utila


def work(
    headnote: str,
    footnote: str,
    pagenumber: str,
    borders: str,
    pages: tuple = None,
) -> str:
    headnote = serializeraw.load_headerfooter(headnote, pages=pages)
    footnote = serializeraw.load_headerfooter(footnote, pages=pages)
    borders = serializeraw.load_pageborders(borders, pages=pages)
    pagenumber = load_pagenumbers(pagenumber, borders, pages=pages)
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
        if pagenumber and pagenumber.footer:
            if not item.header and not item.footer:
                item.header = pagenumber.header
                item.footer = pagenumber.footer
        result.content.append(item)
    return result


def load_pagenumbers(
    pagenumber,
    borders,
    pages: tuple,
) -> iamraw.PageContentFooterHeaders:
    result = iamraw.PageContentFooterHeaders(content=[])
    result.__stategy__ = 'pagenumber'
    loaded = serializeraw.load_pagenumbers(pagenumber, pages=pages)
    single = utila.Single()
    for item in loaded:
        pdfpage = item.pdfpage  # pylint:disable=E1101
        pageborder = utila.select_page(borders, page=pdfpage)
        # TODO: MAY REMOVE LATER
        if single.contains(pdfpage):
            utila.error(f'duplicated pagenumber/pdfpage: {item}')
            continue
        page = create(
            item,
            pdfpage,
            pageborder,
        )
        result.content.append(page)
    return result


def create(item, pdfpage, pageborder) -> iamraw.PageContentFooterHeader:
    pageinfo = iamraw.PageInformation(value=item.detected)  # pylint:disable=E1101
    header, footer = None, None
    begin, end = head_foot_area(pageborder, item.bounding)  # pylint:disable=E1101
    isheader = begin == texmex.START
    if isheader:
        header = iamraw.FixedHeaderInfo(page=pageinfo)
        header.begin = begin
        header.end = end
    else:
        footer = iamraw.FixedFooterInfo(page=pageinfo)
        footer.begin = begin
        footer.end = end
    result = iamraw.PageContentFooterHeader(
        page=pdfpage,
        header=header,
        footer=footer,
    )
    return result


def head_foot_area(pageborder, pagenumber_bounding) -> float:
    pageheight = pageborder.size.height
    if not pageheight:
        utila.error(f'missing page height: {pageborder} {pagenumber_bounding}')
        return texmex.END
    pagenumber_y0 = pagenumber_bounding.y0
    pagenumber_y1 = pagenumber_bounding.y1
    header = pagenumber_y1 < 350
    if header:
        begin = texmex.START
        end = utila.roundme(pagenumber_y1 / pageheight + 0.00)  # TOL
    else:
        # footer
        begin = utila.roundme(pagenumber_y0 / pageheight - 0.01)  # TOL
        end = texmex.END
    return begin, end
