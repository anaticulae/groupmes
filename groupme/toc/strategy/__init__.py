# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import abc
import dataclasses
import typing

import texmex
import utila

import groupme.toc
import groupme.toc.group
import groupme.utils


@dataclasses.dataclass
class ExtractionResult:
    content: typing.List['TocLines'] = dataclasses.field(default_factory=list)
    invalid: typing.List[typing.Any] = dataclasses.field(default_factory=list)

    def __len__(self):
        return len(self.content)

    def __getitem__(self, index):
        return self.content[index]  # pylint:disable=E1136


@dataclasses.dataclass
class ExtractionData:
    content: texmex.PageTextContentNavigators = None


ExtractionResults = typing.List[ExtractionResult]


class ExtractorStrategy(abc.ABC):

    def __init__(self, loaded: ExtractionData):
        self.loaded = loaded

    @abc.abstractmethod
    def result(self) -> ExtractionResult:
        pass


def group(extracted: groupme.toc.TocLines) -> ExtractionResult:
    right, invalid = utila.partition(
        key=lambda x: isinstance(x, groupme.toc.TocLine),
        items=extracted,
    )
    valid = remove_nonconnected_tocs(right)
    for item in right:
        if item not in valid:
            invalid.append(item)
    content = groupme.toc.group.groupby_chapter(valid)
    result = ExtractionResult(content=content, invalid=invalid)
    return result


def create(content: texmex.PageTextContentNavigators) -> ExtractionData:
    data = ExtractionData(content=content)
    return data


def remove_headline(content: texmex.PageTextNavigator) -> texmex.PageTextNavigator:  # yapf:disable
    """Remove table of content headline to improve extraction result."""
    result = texmex.PageTextNavigator(
        pagesize=(content.width, content.height),
        page=content.page,
    )
    for item in content:
        if item.text == 'Inhaltsverzeichnis':
            continue
        result.insert(item.text, item.style, item.bounding)
    return result


def remove_nonconnected_tocs(items):
    """Ensure that toc is connected and not separated by whitepages.
    Select hugest group as single valid table of content."""
    if not items:
        return []
    pagenumbers = [item.raw_location for item in items]
    pagenumbers = sorted(pagenumbers)
    result = [[pagenumbers[0]]]
    for item in pagenumbers[1:]:
        if item > (result[-1][-1] + 1):
            result.append([item])
        else:
            result[-1].append(item)
    valid_pages = set(utila.longest(result))
    # remove non included items
    include = [item for item in items if item.raw_location in valid_pages]
    return include
