# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import serializeraw
import utilotest

import tests


def extract_border(source: str, td, mp) -> set:
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    tests.run(f'-i {source} --border', mp=mp)
    leftright = serializeraw.load_leftright_border(td.tmpdir)
    unique = set(leftright.values())
    return unique


def test_border_diss264(td, mp):
    unique = extract_border(hoverpower.DISS264_PDF, td, mp)
    assert len(unique) == 2, str(unique)
