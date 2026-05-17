#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utilo

import groupmes

DESCRIPTION = 'TODO'

WORKPLAN = [
    utilo.create_step(
        'area',
        inputs=[
            utilo.ResultFile(producer='rawmaker', name='boxes_boxes'),
            utilo.ResultFile(producer='tablero',
                             name='result_result',
                             optional=True),
            utilo.ResultFile(producer='rawmaker', name='text_text'),
            utilo.ResultFile(producer='rawmaker', name='text_positions'),
        ],
        output=('area',),
    ),
    utilo.create_step(
        'border',
        inputs=[
            utilo.ResultFile(producer='rawmaker', name='border_pages'),
            utilo.ResultFile(producer='rawmaker', name='text_positions'),
        ],
        output=('leftright',),
    ),
    utilo.create_step(
        'distance',
        inputs=[
            utilo.ResultFile(producer='groupmes', name='area_area'),
            utilo.ResultFile(producer='rawmaker', name='text_text'),
            utilo.ResultFile(producer='rawmaker', name='text_positions'),
            utilo.ResultFile(producer='groupmes', name='area_area'),
            utilo.ResultFile(producer='rawmaker', name='text_text'),
            utilo.ResultFile(producer='rawmaker', name='text_positions'),
        ],
        output=('distance',),
    ),
    utilo.create_step(
        'content',
        inputs=[
            utilo.ResultFile(producer='rawmaker', name='text_text'),
            utilo.ResultFile(producer='rawmaker', name='text_positions'),
            utilo.ResultFile(producer='rawmaker', name='border_pages'),
            utilo.ResultFile(producer='footnote', name='result_result'),
        ],
        output=('content',),
    ),
    utilo.create_step(
        'hefopa',
        inputs=[
            utilo.ResultFile(producer='headnote', name='result_result'),
            utilo.ResultFile(producer='footnote', name='result_result'),
            utilo.ResultFile(producer='pagenumber', name='result_result'),
            utilo.ResultFile(producer='rawmaker', name='border_pages'),
        ],
        output=('result',),
    )
]


def main():
    utilo.featurepack(
        workplan=WORKPLAN,
        root=groupmes.ROOT,
        featurepackage='groupmes.feature',
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=groupmes.PROCESS,
            pages=True,
            version=groupmes.__version__,
        ),
    )
