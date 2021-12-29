# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power

import groupme

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = groupme.PACKAGE

RESOURCES = [
    power.DISS172_PDF,
    power.MASTER155_PDF,
    power.DISS143_PDF,
    power.BACHELOR128_PDF,
    power.MASTER127_PDF,
    power.BACHELOR111_PDF,
    power.MASTER110_PDF,
    (power.BACHELOR241_PDF, '0:100'),
    power.MASTER091A_PDF,
    power.MASTER089_PDF,
    power.MASTER075_PDF,
    power.MASTER072_PDF,
    power.BACHELOR056_PDF,
    (power.MASTER116_PDF, '50:117'),
    (power.DISS264_PDF, '0:50'),
    (power.DISS406_PDF, '100:150'),
    power.BACHELOR037_PDF,
    (power.MASTER099_PDF, '0:30'),
    (power.MASTER098_PDF, '0:15'),
    (power.BACHELOR090_PDF, '0:25'),
    (power.BACHELOR076_PDF, '0:25'),
    (power.BACHELOR063_PDF, '0:9,59:62'),
    power.DOCU027_PDF,
    power.TECH024_PDF,
    power.HOME018_PDF,
    power.PAPER18_PDF,
    power.DOCU014_PDF,
    genex.todo(power.DOCU007_PDF, tablero=True),
    power.BOOK007_PDF,
    power.DOCU009_PDF,
    (power.BACHELOR051_PDF, '0:25'),
    (power.HOME050_PDF, '0:10'),
    (power.ORDER009_PDF, '0:10'),
    (power.MASTER083_PDF, '0:10'),
    (power.DOCU035_PDF, '0:10'),
    (power.DISS180_PDF, '0:10'),
    (power.DISS205_PDF, '10:20'),
    (power.MASTER078_PDF, '0:10'),
    (power.DISS157_PDF, '6:10'),
]

WORKER = 5


def pytest_sessionstart(session):  # pylint:disable=W0613
    power.run()


def extract(resources):
    destination = power.generated()
    genex.extract(
        resources,
        destination=destination,
        groupme=True,
        worker=WORKER,
        pages=':',
        base=power.REPOSITORY,
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
        groupme=True,
        worker=1,
    )
