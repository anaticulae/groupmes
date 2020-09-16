# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import serializeraw

import tests.groupme_


def footer(source: str, testdir, monkeypatch, pages: str = ':'):
    cmd = f'-i {power.link(source)}  --footer --pages={pages}'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)
    headerpath = iamraw.path.headerfooters(testdir.tmpdir)
    loaded = serializeraw.load_headerfooter(headerpath)
    return loaded
