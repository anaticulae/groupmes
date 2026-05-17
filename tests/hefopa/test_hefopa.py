# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# import hoverpower
# import pytest
# import serializeraw
# import utilo
# import utilotest

# import tests
# import tests.conftest


# @pytest.mark.parametrize(
#     'pdf',
#     utilotest.test_resources(tests.conftest.RESOURCES),
# )
# def test_hefopa(pdf, td, mp):
#     source = hoverpower.link(pdf)
#     cmd = f'-i {source} -o {td.tmpdir} --hefopa'
#     tests.run(cmd, mp=mp)
#     merged = serializeraw.load_headerfooter(td.tmpdir)
#     skip = pdf == hoverpower.BOOK007_PDF  # TODO: ENABLE LATER
#     assert merged or skip


# def test_pagenumbers(td, mp):
#     source = hoverpower.link(hoverpower.HC_DISS193)
#     if not utilo.exists(source):
#         pytest.skip(reason=f'generate: {source}')
#     cmd = f'-i {source} -o {td.tmpdir} --hefopa'
#     tests.run(cmd, mp=mp)
#     merged = serializeraw.load_headerfooter(td.tmpdir)
#     assert len(merged) == 98
