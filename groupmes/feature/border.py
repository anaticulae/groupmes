# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import iamraw
import serializeraw
import utilo

import groupmes.border.leftright
import groupmes.border.most


def work(
    sizeandborder: str,
    textpositions: str,
    pages: tuple = None,
) -> tuple[str]:
    sizeandborder = serializeraw.load_pageborders(sizeandborder, pages=pages)
    textpositions = serializeraw.load_textpositions(textpositions, pages=pages)

    result = determine_border(textpositions, sizeandborder)

    dumped = serializeraw.dump_leftright_border(result)
    return dumped


def determine_border(
    textpositions: iamraw.PageContentTextPositions,
    pagesizes: iamraw.PageSizeBorderList,
):
    clustered = pagecluster(pagesizes)
    result = []
    for pages_incluster in clustered:
        border = cluster_border(textpositions, pagesizes, pages_incluster)
        result.append(border)
    result = utilo.flat(result)
    # sort by page number
    result = sorted(result, key=lambda x: x[0])
    return result


def cluster_border(textpositions, pagesizes, pages_incluster):
    textpositions = utilo.select_pages(textpositions, pages_incluster)
    pagesizes = utilo.select_pages(pagesizes, pages_incluster)

    textpositions = utilo.notnone(textpositions)
    pagesizes = utilo.notnone(pagesizes)

    most = groupmes.border.most.run(pagesizes)
    leftright = groupmes.border.leftright.run(textpositions, pagesizes)

    result = [(page, *expected_border(leftright, most, pagesizes, page))
              for page in pages_incluster]
    return result


def expected_border(leftright, most, pagesizes, page: int):
    # left, right, top, down
    # TODO: CHECK THAT PAGE CALL IS CORRECT
    left = leftright.left
    if isinstance(left, tuple):
        left = left[page % 2]  # pylint:disable=E1136

    right = leftright.right
    if isinstance(right, tuple):
        right = right[page % 2]  # pylint:disable=E1136

    pagesize = utilo.select_page(pagesizes, page).size
    rightborder = pagesize.width - right
    bottomborder = pagesize.height - most.bottom

    result = (left, rightborder, most.top, bottomborder)
    result = utilo.roundme(result)
    return result


PAGE_CLUSTER_SIZE_MIN = configos.HV_INT_PLUS(default=3)

PAGE_CLUSTER_DIFF_MAX = configos.HV_FLOAT_PLUS(default=10.0)


def pagecluster(pagesizes) -> list:

    def equal_size(candidat, clusteritem) -> bool:
        diff = utilo.norms(candidat[0], clusteritem[0])
        return diff < PAGE_CLUSTER_DIFF_MAX

    grouped = utilo.determine_cluster(
        pagesizes,
        classifier=equal_size,
        min_elements=PAGE_CLUSTER_SIZE_MIN,
    )

    pages = [sorted(item.page for item in cluster) for cluster in grouped]
    return pages
