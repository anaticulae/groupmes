# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import groupme.abbreviation
import groupme.abbreviation.parser


def work(
    text: str,
    textposition: str,
    text_oneline: str,
    textposition_oneline: str,
    pages: tuple = None,
) -> str:
    data = load_data(
        text,
        textposition,
        text_oneline,
        textposition_oneline,
        pages,
    )
    parsed = groupme.abbreviation.parser.parse(data)
    # dump result
    dumped = serializeraw.dump_abbreviation_table(parsed)
    return dumped


def load_data(
    text: str,
    textposition: str,
    text_oneline: str,
    textposition_oneline: str,
    pages: tuple = None,
) -> groupme.abbreviation.AbbreviationData:
    normal = serializeraw.ptn_fromfile(
        text=text,
        textpositions=textposition,
        pages=pages,
    )
    oneline = serializeraw.ptn_fromfile(
        text=text_oneline,
        textpositions=textposition_oneline,
        pages=pages,
    )
    data = groupme.abbreviation.AbbreviationData(normal=normal, oneline=oneline)
    return data
