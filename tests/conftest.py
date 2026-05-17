# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import hoverpower
import resinf
import utilotest
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

import groupmes

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = groupmes.PACKAGE

RESOURCES = [
    (hoverpower.BACHELOR241_PDF, '0:100'),
    (hoverpower.DISS264_PDF, '0:50'),
    (hoverpower.HC_DISS193, '0:100'),
    resinf.todo(hoverpower.DOCU007_PDF, tablero=True),
    hoverpower.BACHELOR056_PDF,
    hoverpower.BOOK007_PDF,
    hoverpower.DOCU009_PDF,
    hoverpower.DOCU027_PDF,
    hoverpower.MASTER072_PDF,
    hoverpower.MASTER089_PDF,
    hoverpower.ORDER009_PDF,
]

WORKER = utilotest.worker_count(5, onci=len(RESOURCES))


def pytest_sessionstart(session):  # pylint:disable=W0613
    hoverpower.run()


def extract(resources):
    genex.extract(
        resources,
        pagenumber=True,
        headnote=True,
        footnote=True,
        cleanup=True,
        groupmes=True,
        worker=WORKER,
    )
