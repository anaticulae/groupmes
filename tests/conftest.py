# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import genex
import power
import utila
import utilatest

import groupme

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = groupme.PACKAGE

RESOURCES = [
    (power.MASTER116_PDF, '50:117'),
    (power.MASTER099_PDF, '0:30'),
    (power.MASTER098_PDF, '0:15'),
    (power.BACHELOR090_PDF, '0:25'),
    (power.BACHELOR241_PDF, '0:100'),
    power.MASTER155_PDF,
    power.HOME018_PDF,
    (power.DISS264_PDF, '0:50'),
    (power.MASTER075_PDF),
    (power.BACHELOR056_PDF, '0:55'),
    (power.MASTER089_PDF, '0:89'),
    (power.BACHELOR076_PDF, '0:25'),
    power.MASTER072_PDF,
    power.BACHELOR111_PDF,
    power.BACHELOR037_PDF,
    (power.BACHELOR063_PDF, '0:9,59:62'),
    power.DOCU27_PDF,
    power.TECH024_PDF,
    power.PAPER18_PDF,
    power.DOCU14_PDF,
    power.DOCU07_PDF,
    power.BOOK007_PDF,
    power.DOCU09_PDF,
    (power.MASTER110_PDF, '0:50'),
    (power.BACHELOR051_PDF, '0:25'),
    (power.HOME050_PDF, '0:10'),
    (power.ORDER009_PDF, '0:10'),
    (power.MASTER083_PDF, '0:10'),
    (power.DOCU35_PDF, '0:10'),
]

WORKER = 8


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
    power.DOCU27_PDF,
]


def extract_notitle(resources):
    destination = power.generated(folder='notitle')
    files = [item[0] if isinstance(item, tuple) else item for item in resources]
    # prepare
    without_titlepage = [
        os.path.join(destination, f'{item}.pdf')
        for item in utilatest.simplify_testfile_names(
            files + [power.REPOSITORY],  # ensure correct parent
            sort=False,
        )
    ]
    # jam
    todo = []
    for inpath, outpath in zip(files, without_titlepage):
        todo.append(f'jam -i {inpath} -o {outpath} --remove=0')
    utila.run_parallel(todo)

    # generate
    genex.extract(
        without_titlepage,
        destination,
        groupme=True,
        pages='0:10',
        worker=1,
        base=destination,
    )
