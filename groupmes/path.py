# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def area(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, 'groupmes', 'area_area', prefix)


def border_leftright(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        'groupmes',
        'border_leftright',
        prefix,
    )


def distance(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, 'groupmes', 'distance_distance', prefix)
