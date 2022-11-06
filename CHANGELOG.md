# Changelog

Every noteable change is logged here.

## v0.38.0 (2022-11-06)

### Feature

* add header, footer, pagenumber merging step (078debd3cc3f)

### Chore

* add classifier (359ba436f95f)
* upgrade requirements.txt (0e7b3819b25c)

## v0.37.3 (2022-11-03)

### Chore

* ensure that baw has generated path (166ece5f1dde)
* remove useless page numbers (b430c357ab1c)
* notitle is not required in this project (2d20b40bb19f)
* extend test data generator (0f322125b665)
* convert nightly to all (afab14e265f5)
* upgrade environment (fae2104a174d)
* upgrade requirements.txt (83765c71e918)

## v0.37.2 (2022-10-16)

### Chore

* upgrade pipe library (e67d7f3f97d9)
* upgrade baw (43f30535491a)
* upgrade requirements.txt (039a747e631f)

## v0.37.1 (2022-10-06)

### Chore

* run huge only on Monday (7241bd8766ad)
* root user is not required (9ac1928d9ed7)
* publish generated data if nightly fails (fe64101296f0)
* upgrade requirements.txt (289aa8426992)
* add missing dev resources (6760ecd93281)
* upgrade requirements.txt (4e7914225b6f)

## v0.37.0 (2022-09-29)

### Feature

* use footnote result (7dacbdba4413)
* remove pagenumbers and footer step (21d3f573419e)

### Fix

* skip rotated pages (7b0a14cf36af)

### Documentation

* remove outdated docs (54bc138c4395)

### Chore

* change generator (d6885ce8bad5)
* upgrade requirements.txt (0e142fd5097b)
* reduce resource generator (89bdfcc41410)
* extend test data generator (3ceeb0b416c7)
* add generator step (0720ace1fb47)
* add Jenkinsfile (ef446a9247cc)
* upgrade requirements.txt (75d4b3ed0244)
* upgrade requirements.txt (0b1d6a773970)

## v0.36.1

## v0.36.0

### Feature

* add new pagenumber resource (36d03d613456)

### Fix

* detected raw value is already hidden by cleanup (df1d81f4e788)

## v0.35.0

### Feature

* increase valid footer area (0a6eb469bc43)
* use pdfpage to limit allowed footnote number (edfdb98ccf61)
* improve footnote number finder (a94ac8b83a04)

## v0.34.4

### Feature

* increase valid footer area (21027929c35a)
* log selected footer strategy (db370cf82651)

### Fix

* skip to many invalid footnotes numbers (928759d95c96)

## v0.34.3

### Feature

* increase horizontal diff max (eb650b285328)
* use holy value (758b5befe7bb)

## v0.34.2

### Fix

* allow smaller footnote separators (237df46c9fab)

## v0.34.1

### Feature

* adjust input to new naming (e161eabcfafd)

### Fix

* do not fail on white space line (bb5574ec1aa9)

## v0.34.0

### Feature

* decrease min line merge (48f82d9d8fda)
* add more complex pattern (7a3456db8b3a)

## v0.33.0

### Feature

* connect magic page filler (1d6f709d61c5)
* add page number filling method (906c05b89568)
* add page number improved data port (0b5f3da3e10d)
* do not merge footnotes with too few text at end (c45c97bfe316)
* add result debugging information (2f96983537f3)
* skip footer without any footnote (d42fa4c7e8c6)
* add more debugging information (d9c51835c1dd)

### Fix

* allow single empty footnote merge them later (4bdc1df4c0a6)

## v0.32.0

### Feature

* use hyperlink improver (ed088dc7de2d)
* use improver to improve footnote parser (89abb05adbad)
* add hyperlink improver (a2ca2bae6ea1)

## v0.31.0

### Feature

* improve footnote detection (583081ab95da)

### Fix

* do not add empty highnote (ad4e584e6114)
* fix footnote grouper (307ceaf1cd1f)

## v0.30.0

## v0.29.1

## v0.29.0

### Feature

* use improved decider strategy (0c136eb9c65c)
* add strategy to disable to many invalid detections (0919f08b3607)
* skip multiple page top lines (66d8598599ec)
* introduce raw length to improve toc selector (8e7d3c0dd2de)
* debug decider module (92df84565a6c)
* add page top strategy (a7f485cc474f)
* make separator border adjustable (ecf250b18818)

### Fix

* reduce debugging verbosity (4dc2cb736578)
* adjust configo data type (fca0f4b38111)
* do not include page number into toc content (c69f852cf533)
* remove toc headline of the first page (10268b854176)
* fix very lines at the top of the page (d41d7f049980)
* make page dimension page size dependent (480ca3538e56)
* add # as valid character (643ab7c7cc14)
* adjust to new rawmaker behavior (edcdfd8d3534)

## v0.28.0

### Feature

* filter potential footer horizontals (9d7ac468eb15)
* use common document footer line to reduce hyperlink lines (1e5d7b99db3c)
* add footer horizontals selector (4c8e862119e6)
* remove potential wrong footnote hline which are too right (57189fae72cb)
* increase debugging information (20a27fbe9d4a)

### Fix

* improve line separator selector (999187286c27)
* do not detect date as footnote (9be768146377)

## v0.27.0

### Feature

* add strategy name to extraction result (220ce74a5664)
* debug invalid footer strategy (431e75f376e3)
* do not handle few endnotes as invalid footnotes (7210fee43679)

### Fix

* add missing character (45d80ed949d6)
* adjust min valid footer (e05cbe92142d)

## v0.26.1

### Feature

* add brackets as valid split (550b86c46e3e)

### Fix

* append newline after removing newline in rawmaker (d3c569c06208)
* shrink regex computation time (5e9843a92814)

## v0.26.0

### Feature

* skip pages with too many numbers (26069a2fe3f2)
* split text if required to gather better numbers (95face05bdf7)

### Fix

* adjust raw entry (5d5c8fdab043)

## v0.25.0

### Feature

* use raw field to enable more analyzing later (1494a9b127be)
* add new style concept (1e945074b27c)
* add plus sign as possible user character (a63c7f61556b)
* make footnote parser more strict (59be89cbb9ee)

## v0.24.0

### Feature

* add toc style (ef4fa7b4de24)

### Fix

* ensure that table table starts with headline (733cef8c673a)

## v0.23.0

### Feature

* ensure that first page contain figure table headline (8881ec13e64e)
* use elements headlines list (2a9af7189ccd)
* add English support (b5e5906e3e73)

### Documentation

* adjust interface documentation (c1ae55266c63)

## v0.22.0

### Feature

* run page number extraction twice for wide pages (87e517e9ba90)
* remove small text token trash (a8ceb3527fc4)
* add debugging information (40e55bf1a770)

### Fix

* strip text to improve extraction result (c58e17ff43b7)
* skip None to avoid computation error (e3f663310d41)

### Documentation

* adjust method documentation (0220fef345b0)

## v0.21.0

### Feature

* skip huge text size in potential header (9a320ada3805)
* increase possible word gap at line start (7f1f8d59ef0e)
* make max word dist inline dependent (278087546ac2)

### Fix

* add raw_number to result (fdf10981b7df)

### Documentation

* adjust modules path (2798f58c052a)

## v0.20.0

### Feature

* add option to change remove headlines (17e0121bcfec)
* add balance backup parser (f0399976c54c)
* connect balance strategy (b5202d4b760f)
* add balanced toc parser strategy (c7f43bcf04c0)
* add strategy to group toc lines with errors (621d6bf46a73)
* add regex to determine toc line start and toc line ending (5130cdd20780)
* improve headline skipper (5ac6110df47e)
* use improve style selector (88d3eec4bf2e)
* add special character (78d8e490d14a)
* align white spaces (331f0a8a0fdd)

### Fix

* normalize text to improve extraction behavior (6b1e649be2ba)
* improve extraction result (b72983c79c70)
* adjust figure table parser after enabling balance strategy (bfa92525208e)
* ignore character case (fd8fb7ed0b53)
* do not group empty toc (b09f40c776e8)
* do not fail on empty page (7e70ee7075cf)

## v0.19.0

### Feature

* improve footnote grouping (189db213be34)
* add raw page location (dc702b486ece)
* do not detect more than one page number per page (93c61df5a1b3)
* support None highnotes correctly (9a5eb2d04337)
* move highnote check to separate method (feed63d2a375)
* allow None as valid highnote (7fba1f3211ec)
* disable strategy if too few high notes are parsed (e0c45d208354)
* add no level strategy to group toc with only few level (20341eed18cf)
* add method to detect sections-pattern-toc (d29eebd76e42)
* extend possible toc line pattern (11679c38e84a)
* add attribute raw_level (2559a20346fa)
* use numbered attribute (0df980e7fd5e)
* cache line pattern to reduce execution time (20443da369c1)
* add step wise toc level converter (8fc5281d6db9)
* extend line regex pattern (3d459cf39807)
* use headlines from elements (ff8a841b593a)

### Fix

* improve plain text parser (2625087af2ba)
* footnote error in only a few items (fdb9e2d414c0)
* skip potential footnotes with very short text (7d739a3427c8)
* do not run forever (8e72f642612b)
* split page number from page number (7067f2c7c6ec)

### Documentation

* describe how algorithm work (dd446d514042)
* Happy New Year! (135858f97333)

## v0.18.1

### Feature

* disable header strategy on too few results (055460d2452b)

### Documentation

* Happy New Year! (a2be43289880)

## v0.18.0

### Feature

* support optional seite or page in toc line (1ea946d4cc2f)
* improve headline skipper (1401f3aca24c)
* ensure that matches with correct font size (49d602ad8659)
* add second try strategy (fcdd45212a6a)
* return cluster data for further processing (966b44445e86)
* add support for page numbers with gaps (de89a34e9c0d)
* support [133] as highnote (86e9beaaa147)
* reduce required occurrence to catch lower occurrence (54397ffed2ff)
* use text tolerance to group more in pre selection process (0e0b75b65304)

### Fix

* skip table line as potential header (6cc62b85584d)
* use backup result if first one fails (62ff52016ad1)

### Documentation

* extend interface documentation (6146a1ecf7df)

## v0.17.0

### Feature

* rotate rotated page to use normal header detector (fa44e5e7aaa2)
* simplify code (189734dfe074)
* detected rotated page numbers (c8ce472de634)

### Fix

* add page size (0930b8f2760d)

## v0.16.3

### Feature

* use improved remover (c05723b5fd34)

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
