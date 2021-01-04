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


def test_border_diss264(testdir, monkeypatch):
    source = power.link(power.DISS264_PDF)
    tests.groupme_.run(f'-i {source} --border', monkeypatch=monkeypatch)

    leftright = serializeraw.load_leftright_border(testdir.tmpdir)  # pylint:disable=E1101

    unique = set(leftright.values())
    assert len(unique) == 2, str(unique)
