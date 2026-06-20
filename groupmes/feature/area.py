# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Textual Area
============

TODO:
 * table of content
 * images
 * reference table

"""

import collections
import os

import configos
import serializeraw
import utilo

RECTANGLE_DIFF_MAX = configos.HV_FLOAT_PLUS(default=10.0)

RequiredResources = collections.namedtuple(
    'RequiredResources',
    'textnavigator, tables, boxes',
)

PageContentTextualArea = collections.namedtuple(
    'PageContentTextualArea',
    'page, textual, outside, border',
)
PageContentTextualAreas = list[PageContentTextualArea]


def work(
    boxes: str,
    tables: str,
    text: str,
    textpositions: str,
    pages: tuple = None,
) -> str:
    """Extract different areas out of given data.

    Args:
        boxes(str): path to extract `rawmaker` content boxes
        tables(str): path to extracted `tablero` tables
        text(str): extracted `rawmaker` text
        textpositions(str): positions of extracted text
        pages(tuple): tuple of pages to process
    Returns:
        Dumped extracted areas.
    """
    loaded = load(
        boxes=boxes,
        pages=pages,
        tables=tables,
        text=text,
        textpositions=textpositions,
    )

    grouped = group_areas(loaded=loaded)

    dumped = dump_area(grouped)
    return dumped


def group_areas(loaded: RequiredResources) -> PageContentTextualAreas:
    result = []
    for navigator in loaded.textnavigator:
        page = navigator.page

        tables = utilo.select_page(loaded.tables, page)

        boxes = utilo.select_page(loaded.boxes, page)
        boxes = boxes.content if boxes else None

        grouped = group_page(navigator, tables=tables, boxes=boxes)
        result.append(grouped)
    return result


def group_page(navigator, tables, boxes) -> PageContentTextualArea:
    if tables:
        tables = table_checker(tables)

    if boxes:
        boxes = boxed_checker(boxes)

    textual = []
    inside_tables = []
    inside_boxes = []
    for text in navigator:
        bounding = tuple(text.bounding)
        if tables and tables.contains(*bounding):
            inside_tables.append(bounding)
        if boxes and boxes.contains(*bounding):
            inside_boxes.append(bounding)
        else:
            textual.append(bounding)

    # optimize rectangles
    textual = utilo.rect_merge(textual)
    inside_tables = utilo.rect_merge(inside_tables)
    inside_boxes = utilo.rect_merge(inside_boxes)
    outside = {
        'boxes': inside_boxes,
        'tables': inside_tables,
    }
    border = {
        key: list(value) for key, value in (
            ('boxes', boxes.content if boxes else []),
            ('tables', tables.content if tables else []),
        )
    }
    result = PageContentTextualArea(
        page=navigator.page,
        textual=textual,
        outside=outside,
        border=border,
    )
    return result


def boxed_checker(items) -> utilo.RectangleCheck:
    result = utilo.RectangleCheck(max_diff=RECTANGLE_DIFF_MAX)
    for item in items:
        result.extend(*item.box)
    return result


def table_checker(items) -> utilo.RectangleCheck:
    result = utilo.RectangleCheck(max_diff=RECTANGLE_DIFF_MAX)
    for item in items:
        result.extend(*item.bounding)
    return result


def load(
    boxes: str,
    tables: str,
    text: str,
    textpositions: str,
    pages: tuple = None,
) -> RequiredResources:
    # TODO: SHOULD WE REMOVE HIDDEN ITEMS?
    textnavigator = serializeraw.ptn_fromfile(
        text=text,
        textpositions=textpositions,
        pages=pages,
        state=None,  # load hidden items
    )
    boxes = serializeraw.load_boxes(boxes, pages=pages)
    if os.path.exists(tables):
        tables = serializeraw.load_tables(tables, pages=pages)
    else:
        utilo.log(f'skip using tablero: {tables}, generation is required')
        tables = []
    result = RequiredResources(
        boxes=boxes,
        tables=tables,
        textnavigator=textnavigator,
    )
    return result


def dump_area(items) -> str:
    raw = []
    for page in items:
        outside = {
            key: [utilo.from_tuple(item) for item in value] if value else value
            for key, value in page.outside.items()
        }
        border = {
            key: [utilo.from_tuple(item) for item in border]
                 if border else border for key, border in page.border.items()
        }
        textual = page.textual
        if textual:
            textual = [utilo.from_tuple(item) for item in textual]

        content = {
            'border': border,
            'outside': outside,
            'page': page.page,
            'textual': textual,
        }
        raw.append(content)
    dumped = utilo.yaml_dump(raw)
    return dumped


def load_area(content: str, pages: tuple = None) -> PageContentTextualAreas:
    loaded = utilo.yaml_load(content)
    result = []
    for page in loaded:
        pagenumber = int(page['page'])
        if utilo.should_skip(pagenumber, pages):
            continue
        textual = [utilo.parse_tuple(item) for item in page['textual']
                  ] if page['textual'] else page['textual']
        outside = {
            key: [utilo.parse_tuple(item) for item in values] if values else
                 values for key, values in page['outside'].items()
        }
        border = {
            key: [utilo.parse_tuple(item) for item in values] if values else
                 values for key, values in page['border'].items()
        }
        result.append(
            PageContentTextualArea(
                border=border,
                outside=outside,
                page=pagenumber,
                textual=textual,
            ))
    return result
