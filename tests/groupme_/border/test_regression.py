# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import tests.groupme_


def extract_border(source: str, testdir, monkeypatch) -> set:
    source = power.link(source)
    tests.groupme_.run(f'-i {source} --border', monkeypatch=monkeypatch)
    leftright = serializeraw.load_leftright_border(testdir.tmpdir)
    unique = set(leftright.values())
    return unique


def test_border_diss264(testdir, monkeypatch):
    unique = extract_border(power.DISS264_PDF, testdir, monkeypatch)
    assert len(unique) == 2, str(unique)
