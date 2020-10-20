# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def three_side_equal_cluster(
        todo,
        min_elements: int = 2,
        max_diff=2.0,
        selector=None,
):
    selector = selector if selector else lambda x: x[0]

    def classifier(candidat, clusteritem):

        def matcher(candidat, clusteritem):
            bounding_cluster = selector(clusteritem)
            bounding_test = selector(candidat)

            eqaul = sum([
                utila.near(first, second, diff=max_diff)
                for (first, second) in zip(bounding_test, bounding_cluster)
            ])
            return eqaul >= 3

        return matcher(candidat, clusteritem)

    return utila.classifier.base.determine_cluster(
        todo,
        classifier,
        min_elements=min_elements,
    )


utila.three_side_equal_cluster = three_side_equal_cluster
