# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import utilatest
from utilatest import mp  # pylint:disable=W0611
from utilatest import td  # pylint:disable=W0611

import groupme

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = groupme.PACKAGE

RESOURCES = [
    (power.BACHELOR241_PDF, '0:100'),
    (power.DISS264_PDF, '0:50'),
    (power.ORDER009_PDF, '0:10'),
    genex.todo(power.DOCU007_PDF, tablero=True),
    power.BACHELOR056_PDF,
    power.BOOK007_PDF,
    power.DOCU009_PDF,
    power.DOCU027_PDF,
    power.MASTER072_PDF,
    power.MASTER089_PDF,
]

WORKER = utilatest.worker_count(5, onci=len(RESOURCES))


def pytest_sessionstart(session):  # pylint:disable=W0613
    power.run()


def extract(resources):
    genex.extract(
        resources,
        pagenumber=True,
        cleanup=True,
        groupme=True,
        worker=WORKER,
    )


RESOURCES_NOTITLE = [
    power.DOCU027_PDF,
]


def extract_notitle(resources):
    genex.extract_removepages(
        resources,
        removepages='0',
        folder='notitle',
        pages='0:10',
        pagenumber=True,
        cleanup=True,
        groupme=True,
        worker=1,
    )
