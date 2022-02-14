# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utilatest

import tests.figuretable


@pytest.mark.parametrize('source, pages', [
    pytest.param(
        power.MASTER089_PDF,
        (85, 86, 87, 88),
        id='master89_page85_86_87_88',
    ),
])
@utilatest.nightly
def test_regression_non_valid_examples(source, pages, monkeypatch, testdir):
    source = power.link(source)
    extracted = tests.figuretable.extract_figuretable(
        source,
        pages,
        monkeypatch,
        testdir,
    )
    assert not extracted
