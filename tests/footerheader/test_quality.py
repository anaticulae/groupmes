# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import serializeraw
import utila
import utilatest

import groupme.feature.footer


@utilatest.longrun
def test_footerheader_quality_bachelor111():
    source = power.link(power.BACHELOR111_PDF)
    dumped = groupme.feature.footer.work(
        iamraw.path.text(source),
        iamraw.path.textposition(source),
        iamraw.path.fontheader(source),
        iamraw.path.fontcontent(source),
        iamraw.path.horizontals(source),
        iamraw.path.sizeandborder(source),
        groupme.path.pagenumbers(source),
    )
    result = serializeraw.load_headerfooter(dumped)

    pages = list(range(1, 5))
    selected = [utila.select_page(result, page) for page in pages]

    extracted_pages = [item.page for item in selected]

    assert len(selected) == len(pages)
    assert extracted_pages == pages
    # TODO: ADD VALIDATION HERE
