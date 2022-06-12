#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import re

import setuptools

ROOT = os.path.abspath(os.path.dirname(__file__))
UTF8 = 'utf8'

with open(os.path.join(ROOT, 'README.md'), mode='rt', encoding=UTF8) as fp:
    README = fp.read()

with open(os.path.join(ROOT, 'groupme/__init__.py'), encoding=UTF8) as fp:
    VERSION = re.search(r'__version__ = \'(.*?)\'', fp.read()).group(1)

with open(os.path.join(ROOT, "requirements.txt"), encoding=UTF8) as fp:
    REQUIRES = [line for line in fp.readlines() if line and '#' not in line]

if __name__ == "__main__":
    # allow ssetup.py to run from another directory
    os.chdir(ROOT)
    setuptools.setup(
        author='Helmut Konrad Fahrendholz',
        author_email='info@checkitweg.de',
        description='good old times',
        install_requires=REQUIRES,
        long_description=README,
        name='groupme',
        platforms='any',
        url='https://dev.package.checkitweg.de/groupme',
        version=VERSION,
        zip_safe=False,  # create 'zip'-file if True. Don't do it!
        classifiers=[
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
        packages=[
            'groupme',
            'groupme.border',
            'groupme.feature',
            'groupme.footer',
            'groupme.footer.strategy',
            'groupme.footer.strategy.moving',
            'groupme.footnotes',
            'groupme.footnotes.strategy',
            'groupme.pagenumbers',
        ],
        entry_points={
            'console_scripts': ['groupme = groupme.cli:main',],
        },
    )
