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
