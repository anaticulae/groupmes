# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import groupme.path
import tests.groupme_


def extract_figuretable(source, pages, monkeypatch, testdir):
    pages = ','.join((str(item) for item in pages)) if pages else ''
    pages = f'--pages={pages}' if pages else ''
    cmd = f'-i {source} --figuretable {pages}'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)

    path = groupme.path.figuretable(testdir.tmpdir)
    figuretable = serializeraw.load_toc(path)
    return figuretable
