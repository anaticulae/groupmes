# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw


def merge_footer_pages(footers):
    """Merge following uncompleted footnotes together."""
    # TODO: IMPROVE CHECK IF MERGING IS REQUIRED
    # TODO: MERGE MORE THAN TWO PAGES
    for current, after in zip(footers[0:-1], footers[1:]):
        if (after.page - current.page) != 1:
            # no page neighbours
            continue
        if not after.footer.notes:
            continue
        if not current.footer.notes:
            continue
        if current.footer.notes[-1].number == -1:
            # could not merge, I am not a valid footnote
            continue
        if after.footer.notes[0].number not in (-1, None):
            # no merge required, footnote have a number
            continue
        # merge notes together
        current.footer.notes[-1] = iamraw.FootNoteMerged(
            page=current.footer.notes[-1].page,
            number=current.footer.notes[-1].number,
            notes=[
                current.footer.notes[-1],
                after.footer.notes[0],
            ],
        )
        #update bounding
        # TODO: UPDATE PAGE BOUNDING OVER TWO PAGES MAKES NO SENCE?
        # current.footer.notes[-1].bounding = utila.rectangle_max(
        #     [item.bounding for item in current.footer[-1].notes])
        # remove merged notes from after
        after.footer.notes = after.footer.notes[1:]
    return footers
