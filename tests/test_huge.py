# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import os

import hoverpower
import pytest
import utilo
import utilotest

import tests

# this documents does not passes the current implementation
UNSUPPORTED_DOCUMENTS = {
    # 'paper/page_6_double_column.pdf',
}

EXPECTED_FAILURE = {  # yapf:disable
    # 'docu/twine.pdf': 'font extracting problem',
    # 'docu014': 'not every headlines can be detected',
    # ambigous sections, groupmes works, words does not work
    # 'order/howtowrite_pages9.pdf': 'headline detection does not works correctly',
}


def determine_mark(pdf):
    relative = utilo.file_name(pdf)
    if relative in UNSUPPORTED_DOCUMENTS:
        return pytest.mark.xfail(reason='contains unsupported feature')
    with contextlib.suppress(KeyError):
        return pytest.mark.xfail(reason=EXPECTED_FAILURE[relative])
    return pytest.mark.huge


def params():
    # do not ignore any document, it's a nightly
    ignore = []
    pdf = [
        item for item in hoverpower.PDF if all([
            utilo.file_name(item) not in ignore,
            'notitle' not in item,
        ])
    ]
    result = []
    for item in pdf:
        double = pytest.param(
            (
                item,
                '--char_margin 100.0 --boxes_flow 1.0',
                '--char_margin 5.0 --boxes_flow 1.0 --line_margin 0.3',
            ),
            id=utilo.file_name(item),
            marks=determine_mark(item),
        )
        result.append(double)
    return result


@utilotest.monday
@pytest.mark.parametrize('config', params())
def test_huge_running(config, td, mp):  # pylint:disable=R0914
    pdf, toccmd, generalcmd = config
    tocpath = td.tmpdir.join('toc')
    generalpath = td.tmpdir.join('general')
    for item in [tocpath, generalpath]:
        os.makedirs(item)
    pages = '--pages=0:20'
    rawtoc = f'rawmaker -i {pdf} -j=auto {pages} -o {tocpath} --prefix=oneline {toccmd}'
    rawgeneral = f'rawmaker -i {pdf} -j=auto {pages} -o {generalpath} {generalcmd}'
    utilo.file_copy(pdf, td.tmpdir.join('table'))
    pagenumber = f'pagenumber -i {generalpath} -o {generalpath}'
    groupmes = f'groupmes -i {generalpath} -o {generalpath} --content -j2'
    foonote = f'footnote -i {generalpath} -o {generalpath} -j2'
    cleanup = f'cleanup -i {generalpath} -o {generalpath} -j2'
    tablero = f'tablero -i {generalpath} -o {generalpath} -j3'
    for todo in [
            rawtoc, rawgeneral, pagenumber, foonote, cleanup, groupmes, tablero
    ]:
        done = utilo.run(todo)
        assert done.returncode == utilo.SUCCESS, utilo.format_completed(done)
    current = td.tmpdir.join('current')
    os.makedirs(current)
    # run groupmes
    cmd = f'-i {generalpath} -i {tocpath} -o {current} -j=auto'
    tests.run(cmd, mp=mp)
