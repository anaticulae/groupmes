# changelog

Every noteable change is logged here.

## v0.16.2

### Feature

* detect pagenumbers as a single list (7ae83e0a9eca)

## v0.16.1

### Feature

* introduce holy value (775eb73f141f)

### Fix

* do not use magic parameter (13094613af4a)

## v0.16.0

### Feature

* replace with modifiable holy values (a07de10c3b05)

### Fix

* adjust holy value definition (0fbda91dfd72)
* strip parsed abbreviation (2448577f92f9)

## v0.15.2

### Feature

* skip bad parsing as a result of invalid footer line (ad9a3496cf7e)

### Fix

* add missing page parameter (a4e4fccf4066)

## v0.15.1

### Fix

* update FootNoteMerged bounding (31347d54768e)
* extend invalid abbr list (4b370c81001c)

## v0.15.0

### Feature

* make error notes dependent (2a1b24bdd24e)
* increase potential horizontal line diff (5ab214f7db57)
* merge unconnected footnotes (efb6e22b564d)
* merge both together (0ce3baa56f6e)
* add option to use different footnote parser (5e8c2101510b)
* adjust plain footnote extractor (6e5138af62a0)

### Fix

* round footer start (4d179d53080a)

### Documentation

* extend interface documentation (6b9941aed997)

## v0.14.1

### Fix

* remove senseless check (dd82870eb1b5)

## v0.14.0

### Feature

* replace linero with new tablero (5b2a23547095)
* log skipping tables (6983a84fd210)

## v0.13.1

### Fix

* adjust data type (68308fde905a)

## v0.13.0

### Feature

* add content step to determine ptcn border (008492171238)

### Fix

* add missing rounding (87f097eab5f8)
* adjust header tolerance (84613a15ea42)

## v0.12.0

### Feature

* add option to run collector with lower requirements (575ea57817d0)
* improve common headline parser (57f6efe0e5bb)
* use improved title checker (0f7b0b8532aa)

### Fix

* ensure that header is separated correctly (364bb84b5cc6)

### Documentation

* format docs (686d231f8e30)

## v0.11.1

### Feature

* improve page number detector (89a11628e6f7)

### Fix

* adjust footnote merge algo (0fb9ff1695d1)

## v0.11.0

### Feature

* normalize parsed footnote (29f93d1f93dc)
* do not detect more than one page number per page (0c45ad8bf9fb)
* reduce verbosity (9d40f8ce9ebe)

### Fix

* increase possible indention of second footnotes line (62e173cc3e26)

## v0.10.0

### Feature

* detect page numbers in header area (3e468582efdd)
* decide between normal and rotated pages (61faf84af366)

### Fix

* decide between header and footer (f1198ba5bbb1)

### Documentation

* clarify docs (c8789e3c8129)

## v0.9.2

### Fix

* replace with utila code (703d7f7a7128)

## v0.9.1

### Feature

* dump page to abbr geometry parser (8d1ac2eb8e85)

### Documentation

* extend interface documentation (f4a80bffa64c)

## v0.9.0

### Feature

* skip potential horizontal line which is too right (dc48699749de)
* add page number to parser footnote (006b7fa397e2)

## v0.8.2

## v0.8.1

### Feature

* add footnote bounding to footnote parser (f26136c6371b)

## v0.8.0

### Feature

* make table resource optional (dd325c79c68e)

## v0.7.5

### Feature

* add abbreviation generated path (60b4bd5d674d)

### Fix

* enable longer Arabic numbers in table of content (e379d71a13bd)

## v0.7.4

### Documentation

* move class doc (1936598733a2)

## v0.7.3

### Documentation

* Happy New Year! (7173c3aa3537)

## v0.7.2

## v0.7.1

## v0.7.0

### Feature

* disable toc parser for too few results (e95b1d3dcd06)
* remove start sequence from title (466a305515d5)

### Fix

* adjust min count to pass short documents (a4952f455526)

### Documentation

* fix comment (03af860626a0)

## v0.6.2

## v0.6.1

## v0.6.0

### Feature

* add min content count to plain moving extractor (8e39b7ecb06b)
* improve common header detector (d302e27b2d4f)
* fix footnote parser (04c9f5d9a00b)

## v0.5.1

## v0.5.0

### Feature

* use common cluster to use position instead of repeating content (3707ee19c80c)
* add pagenumber to common header extractor (13b0e0e7d3db)
* add another pages pattern (6c082bcf66c7)
* add quality judgement to prefer common quality (e4886571f137)

### Fix

* add missing count update (5f533d001586)
* add missing import (c4e8284f88c5)
* do not fail on level conversion (944ff9ed18bb)
* do not fail on empty content (005ad94b85eb)
* do not handle date as valid headline level (88bab4a73ab9)

## v0.4.0

### Feature

* use bounding of text to improve text grouping (ae5e862221b3)
* add text bounding to improve footnotes detection (ef38c3409dc4)
* shrink potential footnotes area (b8b30d6f5314)

## v0.3.3

### Fix

* fix dimension of holy value (8494dae179d1)

## v0.3.2

## v0.3.1

### Fix

* fix loading of fewer than 15 pages (52c0f6793cd9)

## v0.3.0

### Feature

* use more generalized toc page selector (a2cd84f49588)
* add option to disable level three selector (4f6761c408e4)
* extend toc level parser with code from words project (e90b2f6a8126)

## v0.2.1

## v0.2.0

### Feature

* support fixed horizontal header on alternating pages (6cc1c5604a60)

## v0.1.1

### Documentation

* move doc code from hey project (1146ff578761)

## v0.1.0

### Feature

* move code from `hey` project (f408d4b38d83)

## v0.0.0 Initial release

