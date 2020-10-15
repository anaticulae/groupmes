# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import utila

MAX_FOOTNOTE_X0 = configo.HolyTable(  # TODO: HOLY VALUE
    items=(
        (440, 100),  # TODO: US Letter?
        (550, 150),  # DINA4
    ),
    left_outranges_none=False,
    right_outranges_none=False,
)


def neighbors(items):
    if not items:
        return []
    result = [[items[0]]]
    for item in items[1:]:
        before = result[-1][-1]
        if connected(before, item):
            result[-1].append(item)
        else:
            result.append([item])
    return result


def connected(first, second):
    # TODO: HOLY VALUE
    leftright = utila.near(first.bounding.x1, second.bounding.x0, diff=20.0)
    # plus indention
    sameorigin = utila.near(first.bounding.x0, second.bounding.x0, diff=25.0)

    sameline = utila.near(first.bounding.y0, second.bounding.y0, diff=5.0)
    underfirst = utila.near(first.bounding.y1, second.bounding.y0, diff=10.0)

    result = (leftright or sameorigin) and (sameline or underfirst)
    return result
