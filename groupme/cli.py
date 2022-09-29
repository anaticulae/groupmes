#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila
from utila import ResultFile
from utila import create_step as step
from utila import featurepack

from groupme import PROCESS
from groupme import ROOT
from groupme import __version__

DESCRIPTION = 'TODO'

WORKPLAN = [
    step(
        'area',
        inputs=[
            ResultFile(producer='rawmaker', name='boxes_boxes'),
            ResultFile(producer='tablero', name='result_result', optional=True),
            ResultFile(producer='rawmaker', name='text_text'),
            ResultFile(producer='rawmaker', name='text_positions'),
        ],
        output=('area',),
    ),
    step(
        'border',
        inputs=[
            ResultFile(producer='rawmaker', name='border_pages'),
            ResultFile(producer='rawmaker', name='text_positions'),
        ],
        output=('leftright',),
    ),
    step(
        'distance',
        inputs=[
            ResultFile(producer='groupme', name='area_area'),
            ResultFile(producer='rawmaker', name='text_text'),
            ResultFile(producer='rawmaker', name='text_positions'),
        ],
        output=('distance',),
    ),
    step(
        'content',
        inputs=[
            ResultFile(producer='rawmaker', name='text_text'),
            ResultFile(producer='rawmaker', name='text_positions'),
            ResultFile(producer='rawmaker', name='border_pages'),
            ResultFile(producer='groupme', name='footer_footerheader'),
        ],
        output=('content',),
    )
]


def main():
    featurepack(
        workplan=WORKPLAN,
        root=ROOT,
        featurepackage='groupme.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=PROCESS,
            pages=True,
            version=__version__,
        ),
    )
