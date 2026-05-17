#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila

import groupmes

DESCRIPTION = 'TODO'

WORKPLAN = [
    utila.create_step(
        'area',
        inputs=[
            utila.ResultFile(producer='rawmaker', name='boxes_boxes'),
            utila.ResultFile(producer='tablero',
                             name='result_result',
                             optional=True),
            utila.ResultFile(producer='rawmaker', name='text_text'),
            utila.ResultFile(producer='rawmaker', name='text_positions'),
        ],
        output=('area',),
    ),
    utila.create_step(
        'border',
        inputs=[
            utila.ResultFile(producer='rawmaker', name='border_pages'),
            utila.ResultFile(producer='rawmaker', name='text_positions'),
        ],
        output=('leftright',),
    ),
    utila.create_step(
        'distance',
        inputs=[
            utila.ResultFile(producer='groupmes', name='area_area'),
            utila.ResultFile(producer='rawmaker', name='text_text'),
            utila.ResultFile(producer='rawmaker', name='text_positions'),
        ],
        output=('distance',),
    ),
    utila.create_step(
        'content',
        inputs=[
            utila.ResultFile(producer='rawmaker', name='text_text'),
            utila.ResultFile(producer='rawmaker', name='text_positions'),
            utila.ResultFile(producer='rawmaker', name='border_pages'),
            utila.ResultFile(producer='footnote', name='result_result'),
        ],
        output=('content',),
    ),
    utila.create_step(
        'hefopa',
        inputs=[
            utila.ResultFile(producer='headnote', name='result_result'),
            utila.ResultFile(producer='footnote', name='result_result'),
            utila.ResultFile(producer='pagenumber', name='result_result'),
            utila.ResultFile(producer='rawmaker', name='border_pages'),
        ],
        output=('result',),
    )
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=groupmes.ROOT,
        featurepackage='groupmes.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=groupmes.PROCESS,
            pages=True,
            version=groupmes.__version__,
        ),
    )
