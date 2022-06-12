# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila


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
        lastone = current.footer.notes[-1]
        # merge notes together
        current.footer.notes[-1] = iamraw.FootNoteMerged(
            page=lastone.page,
            number=lastone.number,
            notes=[
                lastone,
                after.footer.notes[0],
            ],
        )
        #update bounding
        # TODO: UPDATE PAGE BOUNDING OVER TWO PAGES MAKES NO SENCE?
        # current.footer.notes[-1].bounding = utila.rectangle_max(
        #     [item.bounding for item in current.footer[-1].notes])
        # remove merged notes from after
        after.footer.notes = after.footer.notes[1:]
    result = remove_single_footnote_without_number(footers)
    return result


def remove_single_footnote_without_number(footers):
    # remove single footer without any number
    result = []
    for item in footers:
        notes = item.footer.notes
        if len(notes) > 1:
            result.append(item)
            continue
        if len(notes) == 1:
            firstnote = notes[0]
            if firstnote.number in NO_FOOTENOTE_NUMBER:
                utila.verbose(f'remove empty footnote: {notes}')
                continue
            result.append(item)
    return result


NO_FOOTENOTE_NUMBER = (-1, None)
